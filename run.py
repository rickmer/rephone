#!/usr/bin/env python3
from app import create_app
from argparse import ArgumentParser

if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument('--port', type=int, default=5001)
    argparser.add_argument('--debug', action='store_true')
    argparser.add_argument('--demo', action='store_true')
    cmd = argparser.parse_args()
    app = create_app(config_override=dict(demo_mode=cmd.demo))
    app.run(port=cmd.port, debug=cmd.debug)
