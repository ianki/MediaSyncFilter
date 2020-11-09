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

if hasattr(hooks, 'media_file_filter'):
  hooks.media_file_filter.append(media_file_filter)
else:
  # Support for Anki pre-2.1.36
  from aqt.sound import MpvManager, OnDoneCallback, SimpleProcessPlayer
  from aqt import mediasrv
  from anki.sound import AVTag, SoundOrVideoTag

  def wrap_play(self, tag: AVTag, on_done: OnDoneCallback, _old):
    if isinstance(tag, SoundOrVideoTag):
      tag = SoundOrVideoTag(filename=media_file_filter(tag.filename))
    _old(self, tag, on_done)

  def wrap_redirect(path, _old):
    (dirname, path) = _old(path)
    path = media_file_filter(path)
    return dirname, path

  MpvManager.play = wrap(MpvManager.play, wrap_play, 'around')
  SimpleProcessPlayer.play = wrap(SimpleProcessPlayer.play, wrap_play, 'around')
  mediasrv._redirectWebExports = wrap(mediasrv._redirectWebExports, wrap_redirect, 'around')

if hasattr(gui_hooks, 'media_check_will_start'):
  gui_hooks.media_check_will_start.append(media_check_will_start)
else:
  # Support for Anki pre-2.1.36
  from aqt.mediacheck import MediaChecker
  
  def wrap_check(self):
    media_check_will_start()
  
  MediaChecker.check = wrap(MediaChecker.check, wrap_check, 'before')

gui_hooks.sync_will_start.append(sync_will_start)
