import os
import re
import logging
import glob
import ntpath
import pandas as pd
from enum import Enum, unique
from pathlib import Path

# Configure Logging
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent
IWN_DATA_PATH = BASE_DIR / 'data' / 'iwn_data'

class OntologyNode:
    """ An ontology node in IndoWordNet. """
    def __init__(self, node_id, name, abbrev="", examples=""):
        self._node_id = node_id
        self._name = name
        self._abbrev = abbrev
        self._examples = examples

    def node_id(self):
        return self._node_id

    def name(self):
        return self._name

    def abbrev(self):
        return self._abbrev

    def examples(self):
        return self._examples

    def __repr__(self):
        return 'OntologyNode(\'{}\', \'{}\')'.format(self._node_id, self._name)


@unique
class Language(Enum):
    NEPALI = 'nepali'
    ENGLISH = 'english'
    HINDI = 'hindi'

class IndoWordNet:
    """
    Main interface for accessing Indian Language WordNets.
    Adapted for IR Project submission.
    """
    def __init__(self, lang=Language.NEPALI):
        logger.info(f'Loading {lang.value} language synsets...')
        self._synset_idx_map = {}
        self._synset_df = self._load_synset_file(lang.value)
        self._synset_relations_dict = self._load_synset_relations()
        self._load_ontology()
        self._load_lemma_relations()
        self._infer_missing_relations()
        self._hypernym_graph = self._build_hypernym_graph()

    def _load_synset_file(self, lang):
        filename = IWN_DATA_PATH / 'synsets' / f'all.{lang}'
        if not filename.exists():
            logger.warning(f"Synset file not found: {filename}")
            return pd.DataFrame(columns=['synset_id', 'synsets', 'pos'])

        with open(filename, encoding='utf8') as f:
            synsets = list(map(lambda line: self._load_synset(line), f.readlines()))
        
        synset_df = pd.DataFrame(synsets, columns=['synset_id', 'synsets', 'pos'])
        synset_df = synset_df.dropna()
        synset_df = synset_df.set_index('synset_id')
        return synset_df

    def _load_synset_relations(self):
        relations_dict = {}
        # Assuming relations are in IWN_DATA_PATH/synset_relations/*.txt if any
        # The extraction script didn't copy relations files yet because we didn't inspect that folder closely
        # For now, we'll try to load if they exist
        return relations_dict # Placeholder until we copy relation files if needed

    def _infer_missing_relations(self):
        pass # Placeholder

    def _build_hypernym_graph(self):
        return {} # Placeholder

    def _load_ontology(self):
        # Load nodes
        nodes_file = IWN_DATA_PATH / 'ontology' / 'nodes'
        self._ontology_nodes = {}
        if nodes_file.exists():
            for line in open(nodes_file, encoding='utf8'):
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    node_id = int(parts[0])
                    name = parts[1]
                    abbrev = parts[2] if len(parts) > 2 else ""
                    examples = parts[3] if len(parts) > 3 else ""
                    self._ontology_nodes[node_id] = OntologyNode(node_id, name, abbrev, examples)

        # Load map
        map_file = IWN_DATA_PATH / 'ontology' / 'map'
        self._synset_ontology_map = {}
        if map_file.exists():
            for line in open(map_file, encoding='utf8'):
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    synset_id = int(parts[0])
                    # Handle potential non-int formatting in map file
                    try:
                        node_ids = list(map(int, parts[1].split(',')))
                        self._synset_ontology_map[synset_id] = node_ids
                    except:
                        pass
    
    def _load_lemma_relations(self):
        self._antonyms_dict = {}
        self._gradation_dict = {}

    def _update_synset_idx_map(self, synset):
        synset_id = synset.synset_id()
        for word in synset.lemma_names():
            if word in self._synset_idx_map:
                self._synset_idx_map[word].append(synset_id)
            else:
                self._synset_idx_map[word] = [synset_id]
        return True

    def _load_synset(self, synset_string):
        if 'null' in synset_string:
            return None, None, None

        synset_string = synset_string.replace('\n', '').strip()
        synset_pattern = '([0-9]+)\t(.+)\t(.+)\t([a-zA-Z]+)'
        try:
            matches = re.findall(synset_pattern, synset_string)
            if not matches: return None, None, None
            synset_id, synset_words, gloss_examples, pos = matches[0]
        except Exception:
            return None, None, None

        synset_id = int(synset_id)
        synset_words = list(filter(lambda x: x != '', synset_words.split(',')))
        if not synset_words:
            return None, None, None
        head_word = synset_words[0]
        
        gloss = gloss_examples
        examples = []
        if ':"' in gloss_examples:
            parts = gloss_examples.split(':')
            gloss = parts[0]
            if len(parts) > 1:
                examples = ''.join(parts[1:]).replace('"', '').split('  /  ')

        synset = Synset(synset_id, head_word, synset_words, pos, gloss, examples, self)
        self._update_synset_idx_map(synset)

        return synset_id, synset, pos

    def synsets(self, word):
        try:
            synset_id_list = self._synset_idx_map[word]
        except KeyError:
            return []

        synsets = []
        for synset_id in synset_id_list:
            if synset_id in self._synset_df.index:
                synset = self._synset_df.loc[synset_id]['synsets']
                synsets.append(synset)
        return synsets

    def all_synsets(self):
        return list(self._synset_df['synsets'].values)

class Synset:
    def __init__(self, synset_id, head_word, lemma_names, pos, gloss, examples, iwn=None):
        self._synset_id = synset_id
        self._head_word = head_word
        self._lemma_names = lemma_names
        self._pos = pos
        self._gloss = gloss
        self._examples = examples
        self._iwn = iwn

    def __repr__(self):
        return 'Synset(\'{}.{}.{}\')'.format(self._head_word, self._pos, self._synset_id)

    def synset_id(self):
        return self._synset_id

    def lemma_names(self):
        return self._lemma_names

    def definition(self):
        return self._gloss

    def examples(self):
        return self._examples

    def pos(self):
        return self._pos

    def ontology_nodes(self):
        if self._iwn:
            node_ids = self._iwn._synset_ontology_map.get(self._synset_id, [])
            return [self._iwn._ontology_nodes[nid] for nid in node_ids if nid in self._iwn._ontology_nodes]
        return []
