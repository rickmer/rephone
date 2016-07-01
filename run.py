#!/usr/bin/env python3
from app import create_app
from argparse import ArgumentParser
from app.daemon import runner
from os.path import isfile
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
        self.app.run(port=self.cmd.port,
                     host=self.cmd.host,
                     debug=False,
                     threaded=self.cmd.single_threaded)


if __name__ == '__main__':
    # handling command line arguments
    argparser = ArgumentParser(description='rephone - a free telephone call/callback system.')
    # argparser.add_argument('--debug', action='store_true', help="Run with Interactive Debugger")
    argparser.add_argument('--demo', action='store_true', help="Demo Mode; Doesn't make outbound calls.")
    argparser.add_argument('--host', default='localhost', help="Address to listen to")
    argparser.add_argument('--port', type=int, default='5001', help='tcp port to listen to')
    argparser.add_argument('--single_threaded', action='store_false', help='disable multi-threading')
    argparser.add_argument('--block_ip', help='persistent block specific client from dispatch calls')
    argparser.add_argument('--block_phone_number', help='persistent block specific phone number (ITU-T E.164)')
    argparser.add_argument('--config_file', type=str, help="Configuration file")
    subparsers = argparser.add_subparsers()
    interactive = subparsers.add_parser('interactive', help='run in interactive mode')
    interactive.add_argument('interactive', action='store_true', default=True)
    interactive.add_argument('--debug', action='store_true', help="Run with Interactive Debugger")
    start = subparsers.add_parser('start', help='start rephone daemon')
    start.add_argument('start', action='store_true', default=True, help='start the rephone daemon')
    stop = subparsers.add_parser('stop', help='stop rephone daemon')
    stop.add_argument('stop', action='store_true', default=True, help='stop the rephone daemon')
    restart = subparsers.add_parser('restart', help='restart rephone daemon')
    restart.add_argument('restart', action='store_true', default=True, help='restart rephone daemon')
    block = subparsers.add_parser('block', help='block a phone number or ip address')
    block.add_argument('ip_or_phone', choices=['ip', 'phone'], help='persistently block specific client_ip from \
                                                                     dispatch calls or persistently block specific \
                                                                     phone number (ITU-T E.164) from being called')
    block.add_argument('value_to_block', type=str, help='ip address or phonenumber (ITU-T E.164)')
    captcha_gen = subparsers.add_parser('captcha_gen', help='pregen captchas')
    captcha_gen.add_argument('captcha_gen', action='store_true', default=True, help='pregen captchas')
    cmd = argparser.parse_args()

    if 'start' in cmd or 'stop' in cmd or 'restart' in cmd:
        logger = logging.getLogger("RePhoneLog")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler("testdaemon.log")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        daemon_runner = runner.DaemonRunner(DaemonizedApp(cmd=cmd))
        daemon_runner.do_action()
    elif 'interactive' in cmd or 'captcha_gen' in cmd or 'block' in cmd:
        from flask_captcha.helpers import init_captcha_dir, generate_images
        from app.abuse.client import block_ip
        from app.abuse.calls import abuse_detected
        # handling config file
        if cmd.config_file:
            if not isfile(cmd.config_file):
                exit('config file not found')
            else:
                app = create_app(config_override=dict(demo_mode=cmd.demo), config_file=cmd.config_file)
        else:
            app = create_app(config_override=dict(demo_mode=cmd.demo))

        if 'captcha_gen' in cmd and captcha_gen:
            with app.app_context():
                init_captcha_dir()
                generate_images(app.config['CAPTCHA_PREGEN_MAX'])
            exit(0)
        elif 'block' in cmd and cmd.ip_or_phone == 'ip':
            with app.app_context():
                block_ip(cmd.value_to_block)
            exit(0)
        elif 'block' in cmd and cmd.ip_or_phone == 'phone':
            with app.app_context():
                abuse_detected(phone_number=cmd.value_to_block, persist=True)
            exit(0)

        app.run(port=cmd.port,
                host=cmd.host,
                debug=cmd.debug,
                threaded=cmd.single_threaded)











