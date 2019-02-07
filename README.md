# Ant Colony Simulation #

This is a simple *Ant Colony Simulation* game written in Python 3, based on the *PyGame* library. It is largely inspired by previous work of Fabrice Rossi.

## Download & Install ##

First clone the project available on GitHUB under GPL:

```bash
git clone https://github.com/orel33/ants
```

To install Python (root privilege required):

```bash
sudo apt get install python3 pip3
```

To install the *PyGame* module and other useful modules (user privilege enough):

```bash
pip3 install pygame colour bresenham
```

To start the game:

```bash
./main.py
```

## Known Bugs ##

There is a [known bug](https://github.com/pygame/pygame/issues/331) in the *pygame.mixer* module, which causes high CPU usage, when calling *pygame.init()*. A workaround is to disable the mixer module, *pygame.mixer.quit()* or not to enable it, by using *pygame.display.init()* and *pygame.font.init()* instead. Consequently, there is no music, no sound :-(

## Documentation ##

  * https://www.pygame.org
  * http://apiacoa.org/publications/2003/rossi2003swarn-intelligence.pdf (Fabrice Rossi, 2003, GNU/Linux Magazine n° 51)