
from collections import defaultdict
import time
import random

class MapReduceInfo:
    def __init__(self):
        self.logs = []
        
    def log(self, stage, message):
        self.logs.append(f"[{stage}] {message}")

class MapReduceIndexer:
    def __init__(self):
        self.info = MapReduceInfo()

    def mapper(self, doc_id, text):
        """
        Input: doc_id, text
        Output: list of (word, doc_id)
        """
        words = text.lower().split()
        # Simulate processing time
        output = []
        for word in words:
            # Simple tokenization
            clean_word = "".join(c for c in word if c.isalnum())
            if clean_word:
                output.append((clean_word, doc_id))
        return output

    def shuffler(self, mapped_data, num_reducers=3):
        """
        Input: list of (word, doc_id) from all mappers
        Output: dict mapping reducer_id -> list of (word, doc_id)
        """
        shards = defaultdict(list)
        for word, doc_id in mapped_data:
            # Partition by hash of word
            reducer_id = hash(word) % num_reducers
            shards[reducer_id].append((word, doc_id))
        return shards

    def reducer(self, key_word, list_of_doc_ids):
        """
        Input: word, list of doc_ids
        Output: word, posting_list (unique, sorted)
        """
        # Collapse list
        posting_list = sorted(list(set(list_of_doc_ids)))
        return key_word, posting_list

    def run_simulation(self, documents):
        """
        Full MapReduce simulation
        documents: dict of {doc_id: text}
        """
        self.info.logs = []
        self.info.log("MASTER", f"Starting MapReduce Job on {len(documents)} documents")
        
        # 1. Map Phase
        mapped_data = []
        start = time.time()
        for doc_id, text in documents.items():
            result = self.mapper(doc_id, text)
            mapped_data.extend(result)
            self.info.log("MAP", f"Mapped {doc_id}: Generated {len(result)} pairs")
        
        self.info.log("MASTER", f"Map phase finished. Total key-value pairs: {len(mapped_data)}")
        
        # 2. Shuffle Phase
        self.info.log("SHUFFLE", "Partitioning data for Reducers...")
        shards = self.shuffler(mapped_data)
        self.info.log("SHUFFLE", f"Data partitioned into {len(shards)} shards")
        
        # 3. Reduce Phase
        inverted_index = {}
        for reducer_id, items in shards.items():
            # Sort by key for the reducer
            items.sort(key=lambda x: x[0])
            
            # Group by key
            grouped = defaultdict(list)
            for word, doc_id in items:
                grouped[word].append(doc_id)
            
            self.info.log(f"REDUCE-{reducer_id}", f"Processing {len(items)} pairs for {len(grouped)} keys")
            
            for word, doc_ids in grouped.items():
                key, postings = self.reducer(word, doc_ids)
                inverted_index[key] = postings
                
        end = time.time()
        self.info.log("MASTER", f"Job completed in {end - start:.4f} seconds")
        
        return inverted_index, self.info.logs
