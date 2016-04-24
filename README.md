# LightSide
LightSide is intended to be a wake up light making use of BlinkyTape, inspired by James Singleton's
[Pi Glowbe](https://github.com/jpsingleton/pi-glowbe) that I spotted in a copy of 
[MagPi](https://www.raspberrypi.org/magpi/) a few months ago. The name of the project is a reference to a song from
Monty Python's Life of Brian.

## Installation

The prerequisites for using this software are currently Python and some BlinkyTape.

BlinkyTape is a little hard to come by at the moment as [Blinkinlabs](http://blinkinlabs.com/) appears to be out of
stock whenever I have looked. [Adafruit](https://www.adafruit.com/products/1605) is where I managed to find the product
for myself.

Python comes ready installed on many systems but you may want to check the following link for more details,
particularly for Windows or Mac OS X:
[Python 2.7 Installation Guides](http://docs.python-guide.org/en/latest/starting/installation/)

The initial intention in writing this code was to make it work for Python 3.4+ but I need to investigate some
dependency problems before I know that this will work. The current code has therefore only been tested on Python 2.7.
Note also that I have not done any testing on Mac or Windows and so some assumptions and defaults may make it
inappropriate for use on those systems. The main target is intended to be a Raspberry Pi running some flavour of linux.

I also highly recommend the use of `virtualenv` to avoid the need to install LightSide or any of its other
dependencies with root. Although the documentation above makes mention of these, if you are using a linux distribution,
it is probably worth installing `virtualenv` through your normal system package management rather than using the
`pip install virtualenv` command that is suggested.

A command like

```bash
virtualenv lightsideenv
```

will create a virtualenv that is already 'activated' and ready for installing code into. Change to the LightSide
source code directory and install the prerequisites by:

```bash
pip install -r requirements.txt
```

and install LightSide by running:

```bash
python setup.py install
```

You should now be able to run the python code like so:

```bash
lightside wakeup
```

At the moment, the program is only able to run a few preset light programs, with a few command line controls to specify
the duration of the main wakeup transitions. As such, for use as a light to wake you up in the morning, you will need 
to use cron or a similar scheduler to specify when you want the alarm to run. This method might make things a little 
complicated for those who require irregular sleep patterns but for the predictable, you should be able to specify cron 
entries that will work for you for much of the time.

To do this you will need to ensure you know the path to the `lightside` script that is installed into your virtualenv:

```bash
type -P lightside
```

and use that in place of `/path/to/lightside`.

To set up the cron:

```bash
crontab -e
```

then add an entry like:

```
# turn off lights on reboot and just after midnight each night
@reboot /path/to/lightside off 2>&1 >/dev/null
1 0 * * * /path/to/lightside off 2>&1 >/dev/null

# weekdays sunrise starts at 07:15 and weekends at 09:00
15 7 * * MON-FRI /path/to/lightside wakeup 2>&1 >/dev/null
0 9 * * SAT-SUN /path/to/lightside wakeup 2>&1 >/dev/null

```

For further details of what you can do with cron, the [Wikipedia Cron entry](https://en.wikipedia.org/wiki/Cron) looks 
reasonably good.

For options available in `LightSide`, you can run `--help` on the base command and subcommands. At the current time 
there are only two subcommands:

 - `off` is used to turn off the lights and exit.
 - `wakeup` is used to gradually transition from darkness to red to white, stay on for a period and then reverse.
   - `--sunrise-minutes` can be used to set the number of minutes taken to go from off to full brightness
   - `--daytime-minutes` can set the number of minutes the lights stay at maximum brightness
   - `--sunset-minutes` sets the number of minutes taken to go from maximum brightness to off

 - options for all subcommands include:
   - `--port PORT` to specify the blinkytape port
   - `--max-light-level` sets the maximum brightness value
