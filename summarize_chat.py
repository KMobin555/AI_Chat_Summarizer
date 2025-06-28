import os
import argparse
from summarizer import ChatSummarizer

def main():
    parser = argparse.ArgumentParser(description='AI Chat Log Summarizer')
    parser.add_argument('input', help='Path to chat log file or directory')
    parser.add_argument('--output', help='Output file path (optional)')
    parser.add_argument('--nltk', action='store_true', help='Use NLTK for advanced text processing')
    parser.add_argument('--tfidf', action='store_true', help='Use TF-IDF for keyword extraction')

    args = parser.parse_args()

    # print("file path -> " + args.file)

    if not args.output:
        args.output = "output.txt"

    
    print("output path -> " + args.output)

    summarizer_obj = ChatSummarizer(use_nltk = args.nltk, use_tfidf = args.tfidf)

    if os.path.isdir(args.input):
        summaries = summarizer_obj.summarize_directory(args.input)
        # chat = summaries.
        print(summaries)
            
    else:
        chat = summarizer_obj.load_chat(args.input)
        chat = summarizer_obj.generate_summary()
        print(chat)
        

if __name__ == '__main__':
    main()