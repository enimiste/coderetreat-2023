import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import re

class  MyHandler(FileSystemEventHandler):
    def  on_modified(self,  event):
        # print(f'event type: {event.event_type} path : {event.src_path}')
        if re.match('.*/test_(.*)\.py', event.src_path):
            os.system('clear')
            os.system('pytest')
            print('Type <Ctrl+C> to stop the watcher')
            print("Watching for test files changes ...")

    def  on_created(self,  event):
        pass
    
    def  on_deleted(self,  event):
        pass

if __name__=="__main__":
    os.system('clear')
    print("Watching for test files changes ...")
    print('Type <Ctrl+C> to stop the watcher')
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler,  path='.',  recursive=False)
    observer.start()

    try:
        while  True:
            time.sleep(1)
    except  KeyboardInterrupt:
        observer.stop()
        observer.join()