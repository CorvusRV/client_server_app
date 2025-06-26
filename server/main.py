from server.database import Database
from server.app import ServerApp
from server.config import Config
import uvicorn


def main():
    db = Database()
    app = ServerApp(db).app
    uvicorn.run(app, host=Config.S_HOST, port=Config.S_PORT)


if __name__ == "__main__":
    main()
