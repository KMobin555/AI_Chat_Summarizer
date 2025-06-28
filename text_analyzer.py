from collections import defaultdict, Counter
from typing import List, Tuple, Dict 
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import math
from constants import STOPWORDS

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

class TextAnalyzer:
    def __init__(self, use_nltk: bool = False, use_tfidf: bool = False):
        self.use_nltk = use_nltk
        self.use_tfidf = use_tfidf
        self.lemmatizer = WordNetLemmatizer() if use_nltk else None
        self.nltk_stopwords = set(stopwords.words('english')) if use_nltk else None

    def _preprocess_text(self, text: str) -> list[str]:
        
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator).lower()
        
        if self.use_nltk:
            words = word_tokenize(text)
            words = [
                self.lemmatizer.lemmatize(word) 
                for word in words 
                if word not in self.nltk_stopwords and len(word) > 2
            ]
        else:
            words = text.split()
            words = [
                word for word in words 
                if word not in STOPWORDS and len(word) > 2
            ]
        
        return words
    
    def _calculate_tfidf(self, documents: List[List[str]]) -> List[Dict[str,float]]:
        
        tf = []
        idf = defaultdict(int)
        total_docs = len(documents)
        
        for doc in documents:
            doc_tf = defaultdict(int)
            words = self._preprocess_text(' '.join(doc))
            word_count = len(words)
            
            for word in words:
                doc_tf[word] += 1
            
            for word in doc_tf:
                doc_tf[word] /= word_count
            
            tf.append(doc_tf)
            
            for word in set(words):
                idf[word] += 1
        
        for word in idf:
            idf[word] = math.log(total_docs / (1 + idf[word]))
        
        tfidf_scores = []
        for doc_tf in tf:
            doc_tfidf = {}
            for word, tf_val in doc_tf.items():
                doc_tfidf[word] = tf_val * idf[word]
            tfidf_scores.append(doc_tfidf)
        
        return tfidf_scores
    
    def analyze_keywords(self, messages: Dict[str, List[str]], top_n: int = 5) -> List[Tuple[str,float]]:
        
        if self.use_tfidf:
            documents = [messages['user'], messages['ai']]
            tfidf_scores = self._calculate_tfidf(documents)
            
            combined_scores = defaultdict(float)
            for doc_scores in tfidf_scores:
                for word, score in doc_scores.items():
                    combined_scores[word] += score
            
            keywords = sorted(
                combined_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:top_n]
        else:
            all_text = ' '.join(messages['user'] + messages['ai'])
            words = self._preprocess_text(all_text)
            word_counts = Counter(words)
            keywords = word_counts.most_common(top_n)
        
        return keywords


    @staticmethod
    def parse_messages(chat_lines: List[str]) -> Dict[str,list[str]]:

        messages = defaultdict(list)

        for line in chat_lines:
            if line.startswith('User:'):
                messages['user'].append(line[5:].strip())
            elif line.startswith('AI:'):
                messages['ai'].append(line[3:].strip())

        return messages