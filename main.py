import asyncio

from rx import operators
from rx.scheduler.eventloop import AsyncIOScheduler
from rx.subject import Subject
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import url_concat
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.web import RequestHandler, Application, url, StaticFileHandler
from tornado.websocket import WebSocketHandler


def search_wikipedia(term):
    url_ = 'http://en.wikipedia.org/w/api.php'

    params = {
        'action': 'opensearch',
        'search': term,
        'format': 'json'
    }

    user_agent = 'RxPY/3.0 (my agent)'
    url_ = url_concat(url_, params)

    http_client = AsyncHTTPClient()

    res = http_client.fetch(url_, method="GET", user_agent=user_agent)

    print(res)

    return res


class WSHandler(WebSocketHandler):
    def open(self):
        print('socket opened')

        scheduler = AsyncIOScheduler(asyncio.get_event_loop())

        self.subject = Subject()

        searcher = self.subject.pipe(
            operators.map(lambda x: x['term']),
            operators.filter(lambda text: len(text) > 2),
            operators.debounce(0.250),  # 250 ms, waiting user input
            operators.distinct_until_changed(),
            operators.flat_map(search_wikipedia)
        )

        def send_response(x):
            self.write_message(x.body)

        def on_error(ex):
            print(ex)

        searcher.subscribe(send_response, on_error, scheduler=scheduler)

    def on_message(self, message):
        obj = json_decode(message)
        self.subject.on_next(obj)

    def on_close(self):
        print('socket closed')


class MainHandler(RequestHandler):
    def get(self):
        self.render("index.html")


def main():
    AsyncIOMainLoop().make_current()

    port = 8080

    app = Application(
        [url(r"/", MainHandler),
         (r'/ws', WSHandler),
         (r'/static/(.*)', StaticFileHandler, {'path': '.'})
         ]
    )

    app.listen(port)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
