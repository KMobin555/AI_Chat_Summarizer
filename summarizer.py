from file_handler import FileHandler
from text_analyzer import parse_messages

class ChatSummarizer:
    def __init__(self, use_nltk: bool = False, use_tfidf: bool = False):
        self.messages = None
        self.summary = None

    def load_chat(self, file_path = None):
        # if file_path:
        #     self.file_path = file_path

        # if not self.file_path:
        #     raise ValueError("No chat file path provided")

        chat_lines = FileHandler.read_chat_file(file_path)
        self.messages = parse_messages(chat_lines)

        print("parsed message: \n", self.messages)
        return self.messages


    def generate_summary(self):
        if not self.messages:
            self.load_chat()

        total_exchanges = sum(len(msgs) for msgs in self.messages.values())
        user_msg_count = len(self.messages.get('user', []))
        ai_msg_count = len(self.messages.get('ai',[]))


        self.summary = {
            'total_exchanges': total_exchanges,
            'user_message_count': user_msg_count,
            'ai_message_count': ai_msg_count
        }

        return self.summary
    
    def summarize_directory(self, directory_path: str):

        chat_files = FileHandler.process_directory(directory_path)


        return chat_files