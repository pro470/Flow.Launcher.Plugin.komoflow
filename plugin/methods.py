from pyflowlauncher import Method, ResultResponse
from plugin.komorebic_client import WKomorebic


class Query(Method):

    def __init__(self, komorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, query: str) -> ResultResponse:
        return self.return_results()


class Context_menu(Method):

    def __init__(self, komorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, data) -> ResultResponse:
        return self.return_results()
