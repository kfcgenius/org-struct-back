from fastapi import FastAPI

from org_struct_back.settings.server_settings import ServerSettings


class Server:
    def build(self) -> FastAPI:
        raise NotImplementedError()


class ServerImpl(Server):
    def __init__(self, settings: ServerSettings) -> None:
        self._settings = settings

    def build(self) -> FastAPI:
        app = FastAPI()
        return app
