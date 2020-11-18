from __future__ import annotations

import os
import codecs
from collections import defaultdict
from typing import Dict, Set, Tuple
from utils import progressbar
from custom_types import DocumentID, DocumentPath, DocumentBody


class Index:

    def __init__(self, docs: Dict[DocumentID, Tuple[DocumentPath, DocumentBody]]):
        self.docs = docs
        self.keywords = self.build_keyword_document_index(docs)

    @staticmethod
    def build_keyword_document_index(docs: Dict[DocumentID, Tuple[DocumentPath, DocumentBody]]):
        """
        Build a mapping from keyword to all document ids where this keyword is present.

        @params:
            docs - Required: dictionary with documents data
        """
        # Prints are useful, but in real projects logging.Logger is better option
        print("Building document index ...")
        total = len(docs)
        keywords: Dict[str, Set[DocumentID]] = defaultdict(set)
        for i, (doc_id, (path, text)) in enumerate(docs.items(), start=1):
            for word in text.split():
                word = word.strip().lower()
                if word:
                    keywords[word].add(doc_id)
            if not i % 100 or i == total:
                # Progressbar should be used only in the interactive shell
                # In production it can produce a lot of mess in the log file
                progressbar(i, total)
        return keywords

    @staticmethod
    def new(data_path: str) -> Index:
        """
        Construct new search Index.

        Read all files that match pattern *.xml from provided data_path
        and pass them to Index instance.
        @params:
            data_path - Required: path in the filesystem with data files
        """

        print("Reading data files ...")
        docs = {}
        listdir = os.listdir(data_path)[:10]
        total = len(listdir)

        for i, path in enumerate(listdir, start=1):
            if path.endswith('.xml'):
                doc_id = int(path.split(".")[0])
                full_path = os.path.join(data_path, path)
                with codecs.open(full_path, "r", encoding='utf-8', errors='ignore') as f:
                    data = f.read()
                    docs[doc_id] = (path, data)

            if not i % 100 or i == total:
                progressbar(i, total)

        print("Reading data files done.")
        return Index(docs=docs)

    def search(self, phrase: str) -> Set[DocumentID]:
        """
        Search over the index and return document ids that contain ALL words from search phrase.

        @params:
            phrase - Required: search term
        """

        result = None
        # For case insensitive search transform search query to lowercase
        for word in phrase.lower().split():
            if word not in self.keywords:
                # If at least one word was not found in the index result will be empty
                # No sence to check other words
                return set()
            result = result.intersection(self.keywords[word]) if result is not None else self.keywords[word]
            if not result:
                # Result can only shrink by checking additional words, so if it is already empty
                # the final result will be empty too
                return set()
        return result or set()
