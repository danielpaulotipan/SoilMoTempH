#!/bin/sh
sudo python /home/pi/gaswnet.py

# Open terminal
# Type sudo nano /home/pi/launcher.sh
# input the lines of launcher.sh(The code above)
# ctrl x, y, enter.
# in terminal, type cd /home/pi
# type chmod 755 launcher.sh
# type sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart
# input this into the bottom of the file
#@sh /home/pi/launcher.sh
# ctrl x, y, enter.
# sudo reboot
