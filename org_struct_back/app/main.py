from org_struct_back.app.dependency import build_container
from org_struct_back.app.server import Server
from org_struct_back.settings.server_settings import ServerSettings

container = build_container()
settings: ServerSettings = container.resolve(ServerSettings)
server: Server = container.resolve(Server)
app = server.build()
