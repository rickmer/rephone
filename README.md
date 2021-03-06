rephone
=======

Free telephone call/callback system.

[![Build Status](https://travis-ci.org/rickmer/rephone.svg?branch=master)](https://travis-ci.org/rickmer/rephone)
[![Code Climate](https://codeclimate.com/github/rickmer/rephone/badges/gpa.svg)](https://codeclimate.com/github/rickmer/rephone)
[![Stories in Ready](https://badge.waffle.io/rickmer/rephone.png?label=ready&title=Ready)](https://waffle.io/rickmer/rephone)
[![Dependency Status](https://www.versioneye.com/user/projects/5725e5e1ba37ce004309f8b0/badge.svg)](https://www.versioneye.com/user/projects/5725e5e1ba37ce004309f8b0)


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

./rephone start
```
Use your favorite browser: http://localhost:5001

## usage
```
usage: rephone [-h]
               {start,stop,restart,status,interactive,block,captcha_gen} ...

rephone - a free telephone call/callback system.

positional arguments:
  {start,stop,restart,status,interactive,block,captcha_gen}
    start               start rephone daemon
    stop                stop rephone daemon
    restart             restart rephone daemon
    status              prints rephone daemon status
    interactive         run in interactive mode
    block               block a phone number or ip address
    captcha_gen         pregen captchas

optional arguments:
  -h, --help            show this help message and exit
```

```  
usage: rephone start [-h] [--host HOST] [--port PORT] [--single_threaded]
                     [--logfile LOGFILE] [--demo] [--config_file CONFIG_FILE]

positional arguments:
  start                 start the rephone daemon

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Address to listen to
  --port PORT           tcp port to listen to
  --single_threaded     disable multi-threading
  --logfile LOGFILE     logfile to use
  --demo                Demo Mode; Doesn't make outbound calls.
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
