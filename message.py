#!/usr/bin/env python

from defaults import COLORS, ORANGE, RED, ENDC

class Message(object):

  def display_message(self, msg, color='', isBold=False):
    if color:
        print(COLORS[color.upper()] + msg + COLORS["ENDC"])
    else:
        print(msg)

  def warn(self, msg):
      self.display_message(msg, color='orange')

  def yell(self, msg):
      self.display_message(msg, isBold=True, color='red')

  def error(self, msg):
      self.display_message(msg, color='red')

  def notify(self, msg):
      self.display_message(msg)
