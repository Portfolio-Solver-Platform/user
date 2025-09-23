from . import create_app
from .config import Config

app = create_app()


if __name__ == "__main__":
    app.run(host=Config.Flask.HOST, port=Config.Flask.PORT, debug=Config.Flask.DEBUG)
