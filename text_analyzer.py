from collections import defaultdict, Counter
from typing import List, Tuple, Dict 
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class TextAnalyzer:
    def __init__(self, use_nltk: bool = False, use_tfidf: bool = False):
        self.use_nltk = use_nltk
        self.tfidf = use_tfidf
        self.lemmatizer = WordNetLemmatizer() if use_nltk else None
        self.nltk_stoopwords = set(stopwords.words('english')) if use_nltk else None

    @staticmethod
    def parse_messages(chat_lines: List[str]) -> Dict[str,list[str]]:

        messages = defaultdict(list)

        for line in chat_lines:
            if line.startswith('User:'):
                messages['user'].append(line[5:].strip())
            elif line.startswith('AI:'):
                messages['ai'].append(line[3:].strip())

        return messages