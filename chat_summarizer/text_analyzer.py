from collections import defaultdict, Counter
import string
import math
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from typing import List, Tuple, Dict
from chat_summarizer.constants import STOPWORDS 

nltk.download('punkt') 
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')

class TextAnalyzer:
    def __init__(self, use_nltk: bool = False, use_tfidf: bool = False):
        self.use_nltk = use_nltk
        self.use_tfidf = use_tfidf
        self.lemmatizer = WordNetLemmatizer() if use_nltk else None
        self.nltk_stopwords = set(stopwords.words('english')) if use_nltk else None

    def _preprocess_text(self, text: str) -> List[Tuple[str, str]]:

        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator).lower()
        
        if self.use_nltk:
            words = word_tokenize(text)
            # Get POS tags for all words
            tagged_words = pos_tag(words)
            # Filter and lemmatize
            processed = []
            for word, tag in tagged_words:
                if (word not in self.nltk_stopwords and 
                    len(word) > 2 and 
                    word.isalpha()):
                    # Convert POS tag to WordNet format
                    pos = self._get_wordnet_pos(tag)
                    lemma = self.lemmatizer.lemmatize(word, pos) if pos else word
                    processed.append((lemma, tag))
            return processed
        else:
            words = text.split()
            return [(word, '') for word in words 
                    if word not in STOPWORDS 
                    and len(word) > 2 
                    and word.isalpha()]

    def _get_wordnet_pos(self, treebank_tag: str) -> str:

        if treebank_tag.startswith('J'):
            return 'a'  # adjective
        elif treebank_tag.startswith('V'):
            return 'v'  # verb
        elif treebank_tag.startswith('N'):
            return 'n'  # noun
        elif treebank_tag.startswith('R'):
            return 'r'  # adverb
        else:
            return ''  # default (use as is)

    def _calculate_tfidf(self, documents: List[List[str]]) -> Dict[str, float]:


        all_docs = []
        for doc in documents:
            all_docs.extend([msg] for msg in doc)
        
        tf = []
        idf = defaultdict(int)
        total_docs = len(all_docs)
        
        for doc in all_docs:
            doc_tf = defaultdict(int)
            tagged_words = self._preprocess_text(' '.join(doc))
            # Focus more on nouns and proper nouns
            words = [word for word, tag in tagged_words 
                    if tag.startswith('NN') or not self.use_nltk]
            word_count = len(words)
            
            for word in words:
                doc_tf[word] += 1
            
            if word_count > 0:
                for word in doc_tf:
                    doc_tf[word] /= word_count
            
            tf.append(doc_tf)
            for word in set(words):
                idf[word] += 1
        
        tfidf_scores = defaultdict(float)
        for doc_tf in tf:
            for word, tf_val in doc_tf.items():
                idf_score = math.log((total_docs + 1) / (1 + idf[word])) + 1
                tfidf_scores[word] += tf_val * idf_score
        
        return tfidf_scores

    def analyze_keywords(self, messages: Dict[str, List[str]], top_n: int = 5) -> List[Tuple[str, float]]:


        if self.use_tfidf:
            tfidf_scores = self._calculate_tfidf([messages['user'], messages['ai']])
            keywords = sorted(
                tfidf_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:top_n]
        else:
            all_text = ' '.join(messages['user'] + messages['ai'])
            tagged_words = self._preprocess_text(all_text)
            # Focus on nouns for keyword extraction
            words = [word for word, tag in tagged_words 
                    if tag.startswith('NN') or not self.use_nltk]
            word_counts = Counter(words)
            keywords = word_counts.most_common(top_n)
        
        return keywords
    
    @staticmethod
    def parse_messages(chat_lines: List[str]) -> Dict[str, List[str]]:

        messages = defaultdict(list)
        
        for line in chat_lines:
            if line.startswith('User:'):
                messages['user'].append(line[5:].strip())
            elif line.startswith('AI:'):
                messages['ai'].append(line[3:].strip())
        
        return messages

    @staticmethod
    def get_conversation_topics(keywords: List[Tuple[str, float]]) -> str:

        if not keywords:
            return "The conversation had no identifiable topics."
            
        # Take only the top 1-2 most significant topics
        significant_topics = [word for word, score in keywords[:2]]
        
        if len(significant_topics) == 1:
            return f"The conversation was primarily about {significant_topics[0]}."
        else:
            return f"The conversation focused on {significant_topics[0]} and {significant_topics[1]}."
