import os
from typing import List, Dict

class FileHandler:
    @staticmethod
    def read_chat_file(file_path: str) -> List[str]:

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            raise FileNotFoundError(f"chat log file not found at {file_path}")
        except Exception as e:
            raise Exception(f"Error reading chat file: {str(e)}")
        
    @staticmethod
    def process_directory(directory_path: str) -> Dict[str, List[str]]:

        chat_files = {}

        try:
            for filename in os.listdir(directory_path):
                if(filename.endswith('.txt')):
                    file_path = os.path.join(directory_path, filename)
                    chat_files[filename] = FileHandler.read_chat_file(file_path)
        except Exception as e:
            raise Exception(f"Error processing directory: {str(e)}")
        

        return chat_files