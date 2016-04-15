rephone
=======

Free telephone call/callback system.

[![Build Status](https://travis-ci.org/rickmer/rephone.svg?branch=master)](https://travis-ci.org/rickmer/rephone)
[![Code Climate](https://codeclimate.com/github/rickmer/rephone/badges/gpa.svg)](https://codeclimate.com/github/rickmer/rephone)
[![Stories in Ready](https://badge.waffle.io/rickmer/rephone.png?label=ready&title=Ready)](https://waffle.io/rickmer/rephone)


## Project description
We believe in the power of the people and want to contribute that their voices are being heard by decision-makers. Therefore we create an open platform for activists to start calling campaigns to address problems and issues and ask the persons responsible for change. [https://demo.callfordemocracy.org](https://demo.callfordemocracy.org/)


## Installation
```
git clone https://github.com/rickmer/rephone.git
```
Rephone requires gcc-4.8, gcc-4.9 or higher to build due to dependencies in the Python libs.
```
make install
```

## Get Started
```
# activate virtual environment
source bin/activate

./run.py
```
Test web server on your favorite browser: http://localhost:5001

## usage
```
usage: run.py [-h] [--debug] [--demo] [--host HOST] [--port PORT]
              [--single_threaded] [--generate_captcha]
              [--config_file CONFIG_FILE]

rephone - a free telephone call/callback system.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Run with Interactive Debugger
  --demo                Demo Mode; Doesn't make outbound calls.
  --host HOST           Address to listen to
  --port PORT           tcp port to listen to
  --single_threaded     disable multi-threading
  --generate_captcha    (re)generates captcha images
  --config_file CONFIG_FILE
                        Configuration file
```

## Status and contribution

This is a part-time development project... Any contributions preferably [Pull Requests](https://github.com/rickmer/rephone/pulls) are welcome.

You may report any issues or share ideas by using the [Issues](https://github.com/rickmer/rephone/issues) button.

Additionally, there is a chat room on Gitter:
[![Join the chat at https://gitter.im/rickmer/rephone](https://badges.gitter.im/rickmer/rephone.svg)](https://gitter.im/rickmer/rephone?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


## License

[![License](http://www.gnu.org/graphics/agplv3-155x51.png)](http://www.gnu.org/licenses/agpl-3.0.txt)

rephone is provided under the GNU Affero General Public License version 3.
