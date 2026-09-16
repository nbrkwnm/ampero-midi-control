import sys

from app.application import Application

def main() -> int:
    application = Application()

    return application.run()

if __name__ == "__main__":
    sys.exit(main())