"# MediaSyncFilter Anki add-on"

This add-on can be used to optimize Anki's media sync function by filtering out syncing of media in certain conditions.

Settings can be changed in Anki's Add-ons Config settings.  The defaults setting are listed below:

```
  {
    "sync_suspended_cards": false,
    "sync_new_cards": false
  }
```

There are roughly two ways to use this.

a) The default settings will disable syncing of media for cards that are either Suspended or New.  You can use this in the scenario where you usually add and learn new cards on a single computer and then sync to AnkiWeb for review online or on a mobile device.

b) In the scenario where you want to also learn New cards online or on a mobile device, but you keep your cards Suspended until you're ready to learn them, you can change settings to 'sync_suspended_cards': False, 'sync_new_cards': True.

Enjoy!
