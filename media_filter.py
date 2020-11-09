import codecs
import datetime
import importlib
import os
import shutil
import unicodedata

from anki import Collection
from aqt import mw


def printf(msg):
    try:
        print(txt.encode('utf-8'))
    except:
        pass

class MediaFilter:
    def __init__(self):
        self.path_log = os.path.join(mw.pm.profileFolder(), "media_sync_filter.log")
        self.media_dir = os.path.join(mw.pm.profileFolder(), "collection.media")
        self.filter_dir = os.path.join(self.media_dir, "filtered_media")
        if not os.path.exists(self.filter_dir):
            os.mkdir(self.filter_dir)

    def move_files(self, src_path, dst_path, filenames):
        for filename in filenames:
            try:
                src = os.path.join(src_path, filename)
                dst = os.path.join(dst_path, filename)
                if os.path.isfile(src):
                    #printf("move %s to %s" % (src, dst))
                    shutil.move(src, dst)
            except:
                pass

    def on_sync(self, col):
        printf('MediaFilter.on_sync')

        media_dir_files = set(os.listdir(self.media_dir))
        filter_dir_files = set(os.listdir(self.filter_dir))

        config = mw.addonManager.getConfig(__name__)
        print("media sync config is", config)

        skip_queue = -10 if config['sync_suspended_cards'] else -1
        min_reps = 0 if config['sync_new_cards'] else 1

        all_refs = set()
        for nid, mid, flds in col.db.execute(
            "select notes.id, notes.mid, notes.flds from cards, notes"
            " where cards.nid = notes.id and cards.queue != %d"
            " and cards.reps >= %d" % (skip_queue, min_reps)):

            noteRefs = col.media.filesInStr(mid, flds)
            # check the refs are in NFC
            for f in noteRefs:
                # if they're not, we'll need to fix them first
                if f != unicodedata.normalize("NFC", f):
                    col.media._normalizeNoteRefs(nid)
                    noteRefs = col.media.filesInStr(mid, flds)
                    break
            all_refs.update(noteRefs)

        # Move unneeded files to filter dir
        unneded_files = [name for name in media_dir_files.difference(all_refs) if not name.startswith('_')]
        self.move_files(self.media_dir, self.filter_dir, unneded_files)

        # Move needed files back to media dir
        needed_files = filter_dir_files.intersection(all_refs)
        self.move_files(self.filter_dir, self.media_dir, needed_files)

    def on_check_media(self):
        printf('MediaFilter.on_check_media')

        filter_dir_files = set(os.listdir(self.filter_dir))
        self.move_files(self.filter_dir, self.media_dir, filter_dir_files)


def on_sync():
    mf = MediaFilter()
    mf.on_sync(mw.col)

def on_check_media():
    mf = MediaFilter()
    mf.on_check_media()
