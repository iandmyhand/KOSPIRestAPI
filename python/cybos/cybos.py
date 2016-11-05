import logging
import tornado.web

logger = logging.getLogger("tornado.application")


class Cybos(tornado.web.RequestHandler):

    def get_code_by_name(self, constants, name):
        for _constant in constants:
            if _constant[1] == name:
                return _constant[0]
        return None

    def write_error(self, status_code, **kwargs):
        for _kwarg in kwargs:
            logger.error("%s: %s" % (str(_kwarg), str(kwargs.get(_kwarg))))
        self.write("Unknown error occurred: ")
        self.finish()
