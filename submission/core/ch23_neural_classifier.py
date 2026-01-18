
import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import Counter

class SimpleNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        return out

class DocumentClassifierPT:
    def __init__(self, vocab_size=2000):
        self.vocab_size = vocab_size
        self.model = None
        self.vocab = {}
        self.classes = []
        
    def build_features(self, documents):
        """Convert documents to BOW vectors"""
        # Build Vocab if empty
        if not self.vocab:
            all_text = " ".join(documents)
            words = all_text.split()
            common = Counter(words).most_common(self.vocab_size)
            self.vocab = {w: i for i, (w, _) in enumerate(common)}
            
        vectors = []
        for doc in documents:
            vec = np.zeros(len(self.vocab))
            for word in doc.split():
                if word in self.vocab:
                    vec[self.vocab[word]] += 1
            vectors.append(vec)
            
        return torch.FloatTensor(np.array(vectors))
        
    def train(self, documents, labels, epochs=10):
        self.classes = sorted(list(set(labels)))
        class_to_idx = {c: i for i, c in enumerate(self.classes)}
        
        # Prepare Data
        X = self.build_features(documents)
        y = torch.LongTensor([class_to_idx[l] for l in labels])
        
        # Init Model
        input_dim = len(self.vocab)
        output_dim = len(self.classes)
        self.model = SimpleNN(input_dim, 64, output_dim)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        
        history = []
        
        # Training Loop
        self.model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self.model(X)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            
            history.append(loss.item())
            
        return history

    def predict(self, text):
        if not self.model:
            return None
            
        self.model.eval()
        with torch.no_grad():
            vec = self.build_features([text])
            outputs = self.model(vec)
            _, predicted = torch.max(outputs.data, 1)
            return self.classes[predicted.item()]
            
    def retrain(self, new_docs, new_labels, epochs=5):
        """Incremental learning on existing model"""
        if not self.model:
            return self.train(new_docs, new_labels)
            
        # Re-train layers
        self.model.train()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.005) # Lower LR for fine-tuning
        
        classes_map = {c: i for i, c in enumerate(self.classes)}
        
        X = self.build_features(new_docs)
        # Filter unknown labels in streaming context
        valid_indices = [i for i, l in enumerate(new_labels) if l in classes_map]
        if not valid_indices:
            return []
            
        X = X[valid_indices]
        y = torch.LongTensor([classes_map[new_labels[i]] for i in valid_indices])
        
        history = []
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self.model(X)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            history.append(loss.item())
            
        return history
