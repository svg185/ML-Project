import csv, math, re
from collections import Counter, defaultdict
class NaiveBayesIntentClassifier:
    def __init__(self): self.vocab=set(); self.class_counts=Counter(); self.word_counts=defaultdict(Counter); self.total_words=Counter()
    def tok(self,s): return re.findall(r'[a-z0-9]+',s.lower())
    def fit(self,rows):
        for text,label in rows:
            self.class_counts[label]+=1
            for w in self.tok(text): self.vocab.add(w); self.word_counts[label][w]+=1; self.total_words[label]+=1
    def predict(self,text):
        scores={}; total=sum(self.class_counts.values()); V=max(1,len(self.vocab))
        for label,n in self.class_counts.items():
            score=math.log(n/total); denom=self.total_words[label]+V
            for w in self.tok(text): score+=math.log((self.word_counts[label][w]+1)/denom)
            scores[label]=score
        best=max(scores,key=scores.get); m=max(scores.values()); e={k:math.exp(v-m) for k,v in scores.items()}
        return best,e[best]/sum(e.values())
def load_dataset(path):
    with open(path,encoding='utf-8',newline='') as f: return [(r['text'],r['intent']) for r in csv.DictReader(f)]
