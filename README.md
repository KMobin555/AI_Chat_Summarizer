# AI Chat Log Summarizer

A Python tool that summarizes conversations between users and AI assistants, with support for both basic and advanced NLP analysis.

## Features

- Counts total messages and separates by speaker (User/AI)
- Extracts most frequent keywords (excluding common stopwords)
- Generates human-readable summaries
- Supports three analysis modes:
  - Basic word frequency
  - NLTK-enhanced processing
  - TF-IDF analysis
- Processes single files or entire directories
- Outputs results to console or file

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-chat-summarizer.git
   cd ai-chat-summarizer
   ```
2. Create and activate a virtual environment (recommended):

    ```
    python -m venv .venv
    source .venv/bin/activate  # Linux/MacOS
    .venv\Scripts\activate     # Windows
    ```

3. Install requirements:

    ```
    pip install -r requirements.txt
    ```

## Usage
### Basic Command Structure
```
python summarize_chat.py <input_path> [--nltk] [--tfidf] [--output <file>]
```
### Analysis Modes and Example Outputs

1. Basic Mode (Word Frequency)
    ```
    python summarize_chat.py example_texts
    ```
    Example Output:

    ```
    Summary for text1.txt
    Chat Summary:
    - Total Exchanges: 4
    - User messages: 2
    - AI responses: 2
    - The conversation focused on python.
    - Most common keywords: python (3), use (2), tell (1), sure (1), popular (1)
    ```

2. NLTK-Enhanced Mode
    ```
    python summarize_chat.py example_texts --nltk
    ```
    Example Output:

    ```
    Summary for text1.txt
    Chat Summary:
    - Total Exchanges: 4
    - User messages: 2
    - AI responses: 2
    - The conversation focused on python and programming.
    - Most common keywords: python (3), programming (1), language (1), web (1), development (1)
    ```

3. TF-IDF Mode (with NLTK)
    ```
    python summarize_chat.py example_texts --nltk --tfidf
    ```
    Example Output:

    ```
    Summary for text1.txt
    Chat Summary:
    - Total Exchanges: 4
    - User messages: 2
    - AI responses: 2
    - The conversation focused on python and programming.
    - Most common keywords: python (1.88), programming (0.64), language (0.64), web (0.38), development (0.38)
    ```

### Additional Options

* Save output to file:

    ```
    python summarize_chat.py example_texts --nltk --output summary.txt
    ```

* Process a directory of chat logs:
    ```
    python summarize_chat.py path/to/chat_logs/ --nltk
    ```


## Key Differences Between Modes

| Feature               | Basic Mode       | NLTK Mode        | TF-IDF Mode      |
|:----------------------|:----------------:|:----------------:|:----------------:|
| Stopword removal      | Basic list       | NLTK list        | NLTK list        |
| Tokenization          | Simple split     | Advanced         | Advanced         |
| Lemmatization         | No               | Yes              | Yes              |
| POS tagging           | No               | Yes              | Yes              |
| Keyword scoring       | Frequency        | Frequency        | TF-IDF           |
| Topic identification  | Basic            | Improved         | Best             |

## Sample Chat Log Format

* Input file should follow this format:
    ```
    User: Hello!
    AI: Hi! How can I assist you today?
    User: Can you explain what machine learning is?
    AI: Certainly! Machine learning is a field of AI that allows systems to learn from data.
    ```
## Requirements

    * Python 3.7+
    * NLTK (only required for advanced modes)