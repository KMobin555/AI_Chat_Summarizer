from typing import Dict, List, Tuple 
from chat_summarizer.file_handler import FileHandler
from chat_summarizer.text_analyzer import TextAnalyzer

class ChatSummarizer:
    def __init__(self, use_nltk: bool = False, use_tfidf: bool = False):
        self.messages = None
        self.summary = None
        self.text_analyzer = TextAnalyzer(use_nltk=use_nltk,use_tfidf=use_tfidf)

    def load_chat(self, file_path: str) -> Dict[str, List[str]]:
        """Load and parse chat file"""

        chat_lines = FileHandler.read_chat_file(file_path)
        self.messages = self.text_analyzer.parse_messages(chat_lines)

        print("parsed message: \n", self.messages)
        return self.messages


    def generate_summary(self) -> Dict:
        """Generate summary statistics and analysis"""
        if not self.messages:
            raise ValueError("No messages loaded. Call load_chat() first.")

        total_exchanges = len(self.messages['user']) + len(self.messages['ai'])
        user_msg_count = len(self.messages['user'])
        ai_msg_count = len(self.messages['ai'])

        keywords = self.text_analyzer.analyze_keywords(self.messages)
        topics = self.text_analyzer.get_conversation_topics(keywords)


        self.summary = {
            'total_exchanges': total_exchanges,
            'user_message_count': user_msg_count,
            'ai_message_count': ai_msg_count,
            'top_keywords': keywords,
            'topics': topics
        }

        return self.summary
    
    def format_summary(self) -> str:
        """Format summary into human-readable text"""
        if not self.summary:
            self.generate_summary()

        summary_lines = [
            "Chat Summary:",
            f"- Total Exchanges: {self.summary['total_exchanges']}",
            f"- User messages: {self.summary['user_message_count']}",
            f"- AI responses: {self.summary['ai_message_count']}",
            f"- {self.summary['topics']}",
            "- Most common keywords: " + ', '.join(
                [f"{word} ({count})" for word, count in self.summary['top_keywords']]
            )
        ]

        return '\n'.join(summary_lines)
    
    def summarize_directory(self, directory_path: str):
        """Summarize all chat logs in a directory"""

        chat_files = FileHandler.process_directory(directory_path)
        summaries = []

        for filename, chat_lines in chat_files.items():
            self.messages = self.text_analyzer.parse_messages(chat_lines)
            self.generate_summary()
            summaries.append((filename,self.format_summary()))

        return summaries