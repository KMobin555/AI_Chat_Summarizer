from file_utils import read_chat_file

class ChatSummarizer:
    def __init__(self, file_path = None):
        self.file_path = file_path
        self.message = None
        self.summary = None

    def load_chat(self, file_path = None):
        if not file_path:
            raise ValueError("No chat file path provided")

        if file_path:
            self.file_path = file_path

        chat_lines = read_chat_file(self.file_path)
        return chat_lines


        