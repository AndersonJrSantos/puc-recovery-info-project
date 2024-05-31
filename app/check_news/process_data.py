import json
import re
import os
from collections import defaultdict

def clean_text(text):
    # Remove non-alphabetic characters and convert to lowercase
    return re.sub(r'[^a-zA-Z\s]', '', text).lower()

def create_inverted_index(documents):
    inverted_index = defaultdict(list)
    for doc_id, document in enumerate(documents):
        for word in set(clean_text(document['body']).split()):
            inverted_index[word].append(doc_id)
    return inverted_index

def save_inverted_index(inverted_index, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for word, doc_ids in inverted_index.items():
        with open(os.path.join(directory, f'{word}.txt'), 'w') as f:
            f.write(','.join(map(str, doc_ids)))

def main():
    with open('articles.json', 'r') as f:
        articles = json.load(f)

    # Only keep the first 20,000 articles
    articles = articles[:20000]

    inverted_index = create_inverted_index(articles)
    save_inverted_index(inverted_index, 'inverted_index')

if __name__ == '__main__':
    main()
