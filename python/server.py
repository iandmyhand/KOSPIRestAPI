import os
import psutil
import sys
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.log
import tornado.options
import win32api

from cybos.cputil.cpcybos import CpCybosIsConnectHandler
from cybos.cputil.cpcybos import CpCybosServerTypeHandler
from cybos.cputil.cpcybos import CpCybosLimitRequestRemainTimeHandler
from cybos.cputil.cpcybos import CpCybosGetLimitRemainCountHandler
from cybos.cputil.cpstockcode import CpStockCodeCodeToNameHandler
from cybos.cputil.cpstockcode import CpStockCodeNameToCodeHandler
from cybos.cputil.cpstockcode import CpStockCodeCodeToFullCodeHandler
from cybos.cputil.cpstockcode import CpStockCodeFullCodeToNameHandler
from cybos.cputil.cpstockcode import CpStockCodeCodeToIndexHandler
from cybos.cputil.cpstockcode import CpStockCodeGetCountHandler

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
    args.append("--log_rotate_mode=time")
    tornado.options.parse_command_line(args)
    app = tornado.web.Application(
        [
            (r"/", IndexHandler),
            (r"/ping", PingHandler),
            (r"/cpUtil/cpCybos/isConnect", CpCybosIsConnectHandler),
            (r"/cpUtil/cpCybos/serverType", CpCybosServerTypeHandler),
            (r"/cpUtil/cpCybos/limitRequestRemainTime", CpCybosLimitRequestRemainTimeHandler),
            (r"/cpUtil/cpCybos/getLimitRemainCount", CpCybosGetLimitRemainCountHandler),
            (r"/cpUtil/cpStockCode/codeToName", CpStockCodeCodeToNameHandler),
            (r"/cpUtil/cpStockCode/nameToCode", CpStockCodeNameToCodeHandler),
            (r"/cpUtil/cpStockCode/codeToFullCode", CpStockCodeCodeToFullCodeHandler),
            (r"/cpUtil/cpStockCode/fullCodeToName", CpStockCodeFullCodeToNameHandler),
            (r"/cpUtil/cpStockCode/codeToIndex", CpStockCodeCodeToIndexHandler),
            (r"/cpUtil/cpStockCode/getCount", CpStockCodeGetCountHandler),
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
    os.system("taskkill /im python.exe")


if __name__ == "__main__":
    print("PID is " + str(os.getpid()))

    PROCNAME = "python.exe"

    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            if os.getpid() != proc.pid:
                print("kill " + str(proc))
                PROCESS_TERMINATE = 1
                handle = win32api.OpenProcess(PROCESS_TERMINATE, False, proc.pid)
                win32api.TerminateProcess(handle, -1)
                win32api.CloseHandle(handle)

    server = make_server()
    try:
        start_server(server)
    except Exception as e:
        logger.error(str(e))
        stop_server(server)
