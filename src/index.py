import os
import codecs
from collections import defaultdict
from utils import progressbar


class Index:
    # builds a simple keyword-document mapping

    def __init__(self, docs):
        print("Building document index ...")
        total = len(docs)

        self.docs = docs
        self.keywords = defaultdict(set)
        for i, (doc_id, (path, text)) in enumerate(self.docs.items(), start=1):
            for word in text.split():
                word = word.strip().lower()
                if word:
                    self.keywords[word].add(doc_id)
            if not i % 100 or i == total:
                progressbar(i, total)
        print("Building document index done.")

    @staticmethod
    def new(data_path):
        print("Reading data files ...")
        docs = {}
        listdir = os.listdir(data_path)[:10]
        total = len(listdir)
        for i, path in enumerate(listdir, start=1):
            if path.endswith('.xml'):
                doc_id = path.split(".")[0]
                full_path = os.path.join(data_path, path)

                with codecs.open(full_path, "r", encoding='utf-8', errors='ignore') as f:
                    data = f.read()
                    docs[doc_id] = (path, data)
            if not i % 100 or i == total:
                progressbar(i, total)

        print("Reading data files done.")
        return Index(docs=docs)

    def search(self, phrase):
        words = phrase.split()
        results = None
        for word in words:
            word = word.strip().lower()
            if word:
                if word not in self.keywords:
                    continue
                results = self.keywords[word] & results if results is not None else self.keywords[word]
        return results or set()
