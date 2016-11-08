import sys
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.log
import tornado.options

from cybos.cputil import CpCybosIsConnectHandler
from cybos.cputil import CpCybosServerTypeHandler
from cybos.cputil import CpCybosLimitRequestRemainTimeHandler
from cybos.cputil import CpCybosGetLimitRemainCountHandler
from cybos.cputil import CpStockCodeGetCountHandler

logger = logging.getLogger("tornado.application")

# & 'C:\Program Files (x86)\Anaconda3\python.exe' C:\Projects\KOSPIRestAPI\python\server.py


class IndexHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.write({"message": "Hello, world"})
        self.finish()


class PingHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.write({"status": "OK"})
        self.finish()


def make_server():
    logger.info("Making server...")
    args = sys.argv
    args.append("--log_file_prefix=server.log")
    tornado.options.parse_command_line(args)
    app = tornado.web.Application(
        [
            (r"/", IndexHandler),
            (r"/ping", PingHandler),
            (r"/cpUtil/cpCybos/isConnect", CpCybosIsConnectHandler),
            (r"/cpUtil/cpCybos/serverType", CpCybosServerTypeHandler),
            (r"/cpUtil/cpCybos/limitRequestRemainTime", CpCybosLimitRequestRemainTimeHandler),
            (r"/cpUtil/cpCybos/getLimitRemainCount", CpCybosGetLimitRemainCountHandler),
            (r"/cpUtil/cpStockCode/getCount", CpStockCodeGetCountHandler)
        ],
        autoreload=True)
    server = tornado.httpserver.HTTPServer(app)
    return server


def start_server(server):
    logger.info("Starting server...")
    server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    logger.info("Server stopped.")


def stop_server(server):
    server.stop()
    logger.info("Add stop callback.")
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(ioloop.stop)
    logger.info("Maybe server stopping...")


if __name__ == "__main__":
    import os
    print(os.path.dirname(os.path.abspath(__file__)))
    server = make_server()
    try:
        start_server(server)
    except Exception as e:
        logger.error(str(e))
        stop_server(server)
