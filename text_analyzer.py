from collections import defaultdict, Counter

def parse_messages(chat_lines):

    messages = defaultdict(list)

    for line in chat_lines:
        if line.startswith('User:'):
            messages['user'].append(line[5:].strip())
        elif line.startswith('AI:'):
            messages['ai'].append(line[3:].strip())

    return messages