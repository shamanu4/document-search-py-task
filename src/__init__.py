import os
from unicodedata import name
from index import Index
from bottle import route, run, template, static_file, url, Bottle, request

DATA_DIR = 'data'

if __name__ == '__main__':
    app = Bottle()

    index = Index.new(DATA_DIR)

    @app.route('/')
    def search():
        q = request.query.q
        return {
            "results": [
                {
                    "link": request.build_absolute_uri(
                        app.get_url('data_file', filename=index.docs[doc_id][0])
                    ),
                    "id": doc_id
                }
                for doc_id in index.search(str(q))
            ]
        }

    @app.route(f"/{DATA_DIR}/<filename:re:.*\.xml>", name="data_file")
    def data_file(filename):
        return static_file(filename, root=DATA_DIR)
    
    run(app)
