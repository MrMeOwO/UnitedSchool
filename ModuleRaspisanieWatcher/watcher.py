import threading
import hashlib


class ThreadFileWatcher(threading.Thread):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.buffer_size = 65536
        self.hash = ""
        self.func: callable = lambda: print("WARN: FUNC NOT SET")
        self._is_working = True

    def start(self):
        while self._is_working:
            md5 = self.get_file_hash()
            if md5.hexdigest() != self.hash:
                self.hash = md5.hexdigest()
                self.func()

    def stop(self):
        self._is_working = False

    def get_file_hash(self):
        md5 = hashlib.md5()
        with open(self.file_path, 'rb') as f:
            while read_data := f.read(self.buffer_size):
                md5.update(read_data)
        return md5

    def on_file_change(self, func: callable):
        self.func = func
        self.start()
        return func
