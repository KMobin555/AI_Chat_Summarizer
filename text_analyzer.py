from collections import defaultdict, Counter
from typing import List, Tuple, Dict 
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from .constants import STOPWORDS

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class TextAnalyzer:
    def __init__(self, use_nltk: bool = False, use_tfidf: bool = False):
        self.use_nltk = use_nltk
        self.tfidf = use_tfidf
        self.lemmatizer = WordNetLemmatizer() if use_nltk else None
        self.nltk_stoopwords = set(stopwords.words('english')) if use_nltk else None

    def _preprocess_text(self, text: str) -> list[str]:
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator).lower()

        if self.use_nltk:
            words = word_tokenize(text)
            words = [
                self.lemmatizer.lemmatize(word)
                for word in words
                if word not in self.nltk_stoopwords and len(word) > 2
            ]
        else:
            words = text.split()
            words = [
                word for word in words
                if word not in STOPWORDS and len(word) > 2
            ]

        return words


    @staticmethod
    def parse_messages(chat_lines: List[str]) -> Dict[str,list[str]]:

        messages = defaultdict(list)

        for line in chat_lines:
            if line.startswith('User:'):
                messages['user'].append(line[5:].strip())
            elif line.startswith('AI:'):
                messages['ai'].append(line[3:].strip())

        return messages