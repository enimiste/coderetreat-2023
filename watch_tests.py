import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
from os import path
import re

"""
Requirements :
- python 3.9
- pytest==7.4.3
- pytest-cov==4.1.0
- watchdog==3.0.0

Usage : python watch_tests.py [path/to/tests/files/folder]
"""

class  MyHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.has_changes = False

    def  on_modified(self,  event):
        if re.match('.*/test_(.*)\.py', event.src_path):
            self.has_changes = True

    def run_tests(self, dir_or_file_path):
        if self.has_changes:
            dir = dir_or_file_path
            if path.isfile(dir_or_file_path):
                dir = path.dirname(dir_or_file_path)
            os.chdir(dir)
            os.system('pwd')
            os.system("pytest {} --cov".format(dir_or_file_path))
            print("Working dir : " + dir)
            print("Watching for test files changes ...")
            print('Type <Ctrl+C> to stop the watcher')
            self.has_changes = False

    def  on_created(self,  event):
        pass
    
    def  on_deleted(self,  event):
        pass

if __name__=="__main__":
    dir_or_file_path = path.abspath(sys.argv[1] if len(sys.argv)>1 else '.')
    if not path.exists(dir_or_file_path):
        raise RuntimeError("Folder not found : " + dir_or_file_path)
    
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler,  path=dir_or_file_path,  recursive=False)
    observer.start()
    event_handler.has_changes=True # to force first run of tests

    os.system('clear')
    print("Working dir : " + dir_or_file_path)
    print("Watching for test files changes ...")
    print('Type <Ctrl+C> to stop the watcher')

    try:
        while  True:
            event_handler.run_tests(dir_or_file_path)
            time.sleep(1)
    except  KeyboardInterrupt:
        observer.stop()
        observer.join()