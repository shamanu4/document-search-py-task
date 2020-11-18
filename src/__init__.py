import argparse

from index import Index
from bottle import run, static_file, Bottle, request


DATA_DIR = 'data'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Document search service.')
    parser.add_argument('--host', type=str, nargs='?', default='localhost', help='hostname or IP address')
    parser.add_argument('--port', type=int, nargs='?', default=8080, help='port number')
    args = parser.parse_args()

    app = Bottle()
    index = Index.new(DATA_DIR)

    @app.route('/')
    def search():
        q = request.query.q
        return {
            "results": [
                {
                    # This approach looks more appealing, but severily increases
                    # response time when results list is large
                    #
                    # "link": request.build_absolute_uri(
                    #     app.get_url('data_file', filename=index.docs[doc_id][0])
                    # ),
                    #
                    # Use ugly but fast static absolute url generation
                    "link": f"http://{args.host}:{args.port}/{DATA_DIR}/{index.docs[doc_id][0]}",
                    "id": doc_id
                }
                for doc_id in index.search(str(q))
            ]
        }

    @app.route(fr"/{DATA_DIR}/<filename:re:.*\.xml>", name="data_file")
    def data_file(filename):
        return static_file(filename, root=DATA_DIR)

    run(app, host=args.host, port=args.port)
