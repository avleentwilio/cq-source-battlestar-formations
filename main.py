import sys
from cloudquery.sdk import serve

from plugin import FormationsPlugin


def main():
    p = FormationsPlugin()
    serve.PluginCommand(p).run(sys.argv[1:])


if __name__ == "__main__":
    main()
