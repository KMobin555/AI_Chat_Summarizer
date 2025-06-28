import os
import argparse
from chat_summarizer.summarizer import ChatSummarizer

def main():
    parser = argparse.ArgumentParser(description='AI Chat Log Summarizer')
    parser.add_argument('input', help='Path to chat log file or directory')
    parser.add_argument('--output', help='Output file path (optional)')
    parser.add_argument('--nltk', action='store_true', help='Use NLTK for advanced text processing')
    parser.add_argument('--tfidf', action='store_true', help='Use TF-IDF for keyword extraction')

    args = parser.parse_args()


    if not args.output:
        args.output = "output.txt"

    
    # print("output path -> " + args.output)

    # Clear the file contents if it exists, or create it if it doesn't
    with open(args.output, 'w') as f:
        pass 

    summarizer_obj = ChatSummarizer(use_nltk = args.nltk, use_tfidf = args.tfidf)

    if os.path.isdir(args.input):
        summaries = summarizer_obj.summarize_directory(args.input)
        
        for filename, summary in summaries:
            print(f"\nSummary for {filename}")
            print(summary)
            if args.output:
                with open(args.output, 'a') as f:
                    f.write(f"\nSummary for {filename}:\n{summary}\n")

        print(f"The output saved at {args.output}")
            
    else:
        summarizer_obj.load_chat(args.input)
        summary = summarizer_obj.format_summary()
        print(summary)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(summary)

        print(f"The output saved at {args.output}")
        

if __name__ == '__main__':
    main()