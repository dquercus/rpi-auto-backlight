#!/usr/bin/env python

import os
import sys
import syslog
import time
import RPi.GPIO as GPIO

import configparser
from rpi_backlight import Backlight

class AutoBrightness:
  def __init__(self):
    """
        Read config file and stores
    """
    try:
      config_path = os.environ["AUTO_BRIGHTNESS_CONFIG_FILE"]
    except:
      syslog.syslog("Using default config path /etc/auto_brighness.cfg")
      config_path = "/etc/auto_brighness.cfg"

    config = configparser.ConfigParser()
    config.read(config_path)

    self.__port = config['default'].getint('RPI_PORT', '7')
    syslog.syslog("Using RPI_PORT="+str(self.__port))

    self.__brightnessOnDark = int(config['default'].get('DARK_BRIGHTNESS', '5'))
    syslog.syslog("Using DARK_BRIGHTNESS="+str(self.__brightnessOnDark))

    self.__brightnessOnLight = int(config['default'].get('LIGHT_BRIGHTNESS', '90'))
    syslog.syslog("Using LIGHT_BRIGHTNESS="+str(self.__brightnessOnLight))

    self.__loopPause = int(config['default'].get('LOOP_PAUSE', '2'))
    syslog.syslog("Using LOOP_PAUSE="+str(self.__loopPause))

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.__port,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  def set_brighness_level(self,level):
    """
     Change screen brightness to value givin as parameter
    """

    backlight = Backlight()
    backlight.brightness = level

  def main_loop(self):

    syslog.syslog("Starting loop. Waiting for input from sensor.")
    last_state = False

    while(True):
      current_state = GPIO.input(self.__port)

      if (current_state != last_state):
        if (current_state == True):
          syslog.syslog("Light below threshold => dimming down screen")
          self.set_brighness_level(5)
        else:
          syslog.syslog("Light threshold reached => dimming up screen")
          self.set_brighness_level(90)

        last_state = current_state

      time.sleep(self.__loopPause); # Sleep for a full second before restarting our loop


# Star program by going to main loop.

syslog.syslog("starting Automatic Bright Adjustement deamon")
object = AutoBrightness()
object.main_loop()
