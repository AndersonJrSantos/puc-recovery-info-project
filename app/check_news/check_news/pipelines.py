# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import os
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

class CheckNewsPipeline:
    def open_spider(self, spider):
        self.documents = []
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('portuguese'))

    def process_item(self, item, spider):
        if 'body' in item and isinstance(item['body'], str):
            cleaned_body = self.clean_text(item['body'])
            self.documents.append({'title': item['title'], 'body': cleaned_body})
        return item

    def close_spider(self, spider):
        inverted_index = self.create_inverted_index(self.documents)
        self.save_inverted_index(inverted_index, 'inverted_index')

    def clean_text(self, text):
        text = re.sub(r'[^a-zA-Záéíóúãõâêîôûç\s]', '', text).lower()
        return ' '.join(word for word in text.split() if word not in self.stop_words)

    def create_inverted_index(self, documents):
        inverted_index = defaultdict(list)
        for doc_id, document in enumerate(documents):
            for word in set(document['body'].split()):
                inverted_index[word].append(doc_id)
        return inverted_index

    def save_inverted_index(self, inverted_index, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        for word, doc_ids in inverted_index.items():
            with open(os.path.join(directory, f'{word}.txt'), 'w') as f:
                f.write(','.join(map(str, doc_ids)))
