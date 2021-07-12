import sys

from .app import create_app

if __name__ == '__main__':
    create_app().run(
        host=sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1",
        port=8000,
        debug=True
    )
