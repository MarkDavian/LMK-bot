import glob
import os

from config import settings


PATH = settings.files['path']


class File(str):
    def __new__(cls, filename: str):
        self = FileNameResolver(filename).resolve()

        return PATH+self


class FileNameResolver:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.fileResolver = FileResolver()

    def resolve(self):
        name, ext = self.filename.split('.')

        if os.path.exists(PATH+self.filename):
            count = self.count_same_files(name)
            return f"{name}_{count}.{ext}"
        else:
            return self.filename

    def count_same_files(self, name: str):
        count = len(glob.glob1(PATH, name+'*'))
        return count


class FileResolver:
    def __init__(self) -> None:
        self.files_mx_count = settings.files['max-count']
