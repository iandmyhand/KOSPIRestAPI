import sys
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.log
import tornado.options

from cybos.cputil import CpCybosIsConnectHandler
from cybos.cputil import CpStockCodeGetCountHandler

logger = logging.getLogger("tornado.application")


class IndexHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.write("Hello, world")
        self.finish()


def make_server():
    logger.info("Making app...")
    args = sys.argv
    args.append("--log_file_prefix=app.log")
    tornado.options.parse_command_line(args)
    app = tornado.web.Application(
        [
            (r"/", IndexHandler),
            (r"/cpUtil/cpCybos/isConnect", CpCybosIsConnectHandler),
            (r"/cpUtil/cpStockCode/getCount", CpStockCodeGetCountHandler)
        ],
        autoreload=False)
    server = tornado.httpserver.HTTPServer(app)
    return server


def start_server(server):
    logger.info("Starting app...")
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    logger.info("App stopped.")


def stop_server(server):
    server.stop()
    logger.info("Add stop callback.")
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(ioloop.stop)
    logger.info("Maybe server stopping...")


if __name__ == "__main__":
    server = make_server()
    try:
        start_server(server)
    except Exception as e:
        logger.error(str(e))
        stop_server(server)
