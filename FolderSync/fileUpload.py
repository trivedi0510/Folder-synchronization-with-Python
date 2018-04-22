# The following script uses watchdog which helps in firing an event whenever
# a directory undergoes any modification. Whenever a new file/directory is created
# we push the change onto dropbox which will help us in synchronizing contents across
# various systems.

# This script has to be run in the background as a daemon.

try:
    import os
    import sys
    import dropbox
    #from dropbox.client import DropboxClient
    from config import ACCESS_TOKEN, LOCAL_DIRECTORY_WATCH, DROPBOX_SYNC_LOCATION
    import time
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

except Exception as e:
    print e

client = dropbox.Dropbox(ACCESS_TOKEN)


class MyHandler(FileSystemEventHandler):
    # event which gets fired whenever our specifies directory undergoes any change
    # specify the directory name to be watched in the config.py file

    def on_modified(self, event):
        for root, dirs, files in os.walk(LOCAL_DIRECTORY_WATCH):
            for filename in files:
                local_path = os.path.join(root, filename)
                print(local_path)
                DROP_BOX_PATH = local_path.replace(LOCAL_DIRECTORY_WATCH,"").replace("\\","/")
                print(DROP_BOX_PATH, local_path)
                try:
                    with open(local_path, 'rb') as f:
                        data = f.read()
                    client.files_upload(data, DROP_BOX_PATH, mode=dropbox.files.WriteMode.overwrite)
                except Exception as e:
                    print e


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=LOCAL_DIRECTORY_WATCH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()