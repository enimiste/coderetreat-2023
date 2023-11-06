import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import re

"""
Requirements :
- python 3.9
- pytest==7.4.3
- pytest-cov==4.1.0
- watchdog==3.0.0
"""

class  MyHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.has_changes = False

    def  on_modified(self,  event):
        # print(f'event type: {event.event_type} path : {event.src_path}')
        if re.match('.*/test_(.*)\.py', event.src_path):
            self.has_changes = True

    def run_tests(self):
        if self.has_changes:
            os.system('clear')
            os.system('pytest --cov')
            print('Type <Ctrl+C> to stop the watcher')
            print("Watching for test files changes ...")
            self.has_changes = False

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
            event_handler.run_tests()
            time.sleep(1)
    except  KeyboardInterrupt:
        observer.stop()
        observer.join()