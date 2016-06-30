#!/usr/bin/env python3
from app import create_app
from argparse import ArgumentParser
from os.path import isfile
from app.daemon import runner
import logging


class DaemonizedApp(object):

    def __init__(self,
                 cmd,
                 stdin='/dev/null',
                 stdout='/dev/tty',
                 stderr='/dev/tty',
                 pidfile_path='/var/lock/rephone.pid'):
        self.cmd = cmd
        self.stdin_path = stdin
        self.stdout_path = stdout
        self.stderr_path = stderr
        self.pidfile_path = pidfile_path
        self.pidfile_timeout = 5

        if cmd.config_file:
            if not isfile(cmd.config_file):
                exit('config file not found')
            else:
                self.app = create_app(config_override=dict(demo_mode=cmd.demo), config_file=cmd.config_file)
        else:
            self.app = create_app(config_override=dict(demo_mode=cmd.demo))

    def run(self):
        self.app.run(port=cmd.port,
                     host=cmd.host,
                     debug=cmd.debug,
                     threaded=cmd.single_threaded)


def interactive():
    from flask_captcha.helpers import init_captcha_dir, generate_images
    from app.abuse.client import block_ip
    from app.abuse.calls import abuse_detected
    from os.path import isfile
    # handling config file
    if cmd.config_file:
        if not isfile(cmd.config_file):
            exit('config file not found')
        else:
            app = create_app(config_override=dict(demo_mode=cmd.demo), config_file=cmd.config_file)
    else:
        app = create_app(config_override=dict(demo_mode=cmd.demo))

    if cmd.command == 'captcha-gen':
        with app.app_context():
            init_captcha_dir()
            generate_images(app.config['CAPTCHA_PREGEN_MAX'])
        exit(0)
    elif cmd.block_ip:
        with app.app_context():
            block_ip(cmd.block_ip)
        exit(0)
    elif cmd.block_phone_number:
        with app.app_context():
            abuse_detected(phone_number=cmd.block_phone_number, persist=True)
        exit(0)

    app.run(port=cmd.port,
            host=cmd.host,
            debug=cmd.debug,
            threaded=cmd.single_threaded)

if __name__ == '__main__':
    # handling command line arguments
    argparser = ArgumentParser(description='rephone - a free telephone call/callback system.')
    argparser.add_argument('--debug', action='store_true', help="Run with Interactive Debugger")
    argparser.add_argument('--demo', action='store_true', help="Demo Mode; Doesn't make outbound calls.")
    argparser.add_argument('--host', default='localhost', help="Address to listen to")
    argparser.add_argument('--port', type=int, default='5001', help='tcp port to listen to')
    argparser.add_argument('--single_threaded', action='store_false', help='disable multi-threading')
    argparser.add_argument('--block_ip', help='persistent block specific client from dispatch calls')
    argparser.add_argument('--block_phone_number', help='persistent block specific phone number (ITU-T E.164)')
    argparser.add_argument('--config_file', type=str, help="Configuration file")
    argparser.add_argument('command', type=str, nargs='?', default='interactive', help="start, stop, restart, captcha-gen, interactive")
    cmd = argparser.parse_args()

    if cmd.command in ['start', 'stop', 'restart']:
        logger = logging.getLogger("DaemonLog")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler("testdaemon.log")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        daemon_runner = runner.DaemonRunner(DaemonizedApp(cmd=cmd))
        daemon_runner.do_action()
    else:
        interactive()











