def read_chat_file(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"chat log file not found at {file_path}")
    except Exception as e:
        raise Exception(f"Error reading chat file: {str(e)}")