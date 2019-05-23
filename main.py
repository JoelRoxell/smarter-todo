import os

import smartertodo.cli

if os.environ.get('LC_CTYPE', '') == 'UTF-8':
    os.environ['LC_CTYPE'] = 'en_US.UTF-8'


def main():
    smartertodo.cli.run()


if __name__ == '__main__':
    main()
