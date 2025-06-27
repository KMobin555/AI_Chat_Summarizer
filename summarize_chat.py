import argparse

def main():
    parser = argparse.ArgumentParser(description='AI Chat Log Summarizer')
    parser.add_argument('file', help = 'Path to chat log file')
    parser.add_argument('--output', help = 'Output file path (optional)')

    args = parser.parse_args()

    print("file path -> " + args.file)

    if not args.output:
        args.output = "output.txt"

    
    print("output path -> " + args.output)


if __name__ == '__main__':
    main()