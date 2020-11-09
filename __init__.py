# -*- coding: utf-8 -*-

import importlib
import os

from anki import media, hooks
from anki.hooks import wrap
from anki.hooks import addHook
from aqt import gui_hooks, mw

def sync_will_start():
  from . import media_filter
  importlib.reload(media_filter)
  return media_filter.on_sync()

def media_check_will_start():
  from . import media_filter
  importlib.reload(media_filter)
  return media_filter.on_check_media()

def my_redirect_path(self, path, _old):
  from . import media_filter
  importlib.reload(media_filter)
  return media_filter.redirect_path(self, path, _old)

def media_file_filter(file_path):
  full_path = os.path.join(mw.pm.profileFolder(), file_path)
  if not os.path.exists(full_path):
    alt_path = os.path.join('hidden', file_path)
    full_path = os.path.join(mw.pm.profileFolder(), alt_path)
    if os.path.exists(alt_path):
        file_path = alt_path

  return file_path

gui_hooks.sync_will_start.append(sync_will_start)
gui_hooks.media_check_will_start.append(media_check_will_start)
hooks.media_file_filter.append(media_file_filter)
