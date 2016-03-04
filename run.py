#!/usr/bin/env python3
from app import create_app
from argparse import ArgumentParser

if __name__ == '__main__':
    argparser = ArgumentParser(description='rephone - a free telephone call/callback system.')
    argparser.add_argument('--debug', action='store_true', help="Run with Interactive Debugger")
    argparser.add_argument('--demo', action='store_true', help="Demo Mode; Doesn't make outbound calls.")
    argparser.add_argument('--port', type=int, default='5001', help='tcp port to listen to')
    cmd = argparser.parse_args()
    app = create_app(config_override=dict(demo_mode=cmd.demo))
    app.run(port=cmd.port, debug=cmd.debug)
