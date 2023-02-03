import os
import platform
import glob
import logging


from config import settings


resolver_logger = logging.getLogger(__name__)
resolver_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/FileResolver.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
resolver_logger.addHandler(handler)
resolver_logger.addHandler(logging.StreamHandler())


PATH = settings.files['path']
MAX = settings.files['max-count']


class File(str):
    def __new__(cls, filename: str):
        self = FileNameResolver(filename).resolve()

        return PATH+self


class FileNameResolver:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.fileResolver = FileResolver()

    def resolve(self):
        resolver_logger.info(f'Resolving filename {self.filename}')
        name, ext = self.filename.split('.')

        if self.fileResolver.more_than_max_count():
            self.fileResolver.delete_one()

        if os.path.exists(PATH+self.filename):
            count = self.count_same_files(name)
            return f"{name}_{count}.{ext}"
        else:
            return self.filename

    def count_same_files(self, name: str):
        count = len(glob.glob1(PATH, name+'*'))
        return count


class FileResolver:
    def more_than_max_count(self) -> bool:
        files = glob.glob(PATH+'*')
        if len(files) >= MAX:
            return True
        return False

    def delete_one(self) -> None:
        filename = self.get_the_oldest()
        self._delete(filename)

    def delete_many(self, count: int) -> None:
        dates, date_to_file = self._get_dates_and_files()
        if count >= dates:
            count = len(dates)

        files = date_to_file[len(dates)-count:-1]
        
        for file in files:
            self._delete(file)

    def get_the_oldest(self) -> str:
        dates, date_to_file = self._get_dates_and_files()

        return date_to_file[dates[0]]

    def _get_dates_and_files(self) -> tuple[list[str], dict]:
        files = glob.glob(PATH+'*')
        date_to_file = {}
        dates = []
        for file in files:
            cr_date = self.creation_date(file)
            date_to_file[cr_date] = file
            dates.append(cr_date)

        dates.sort()
        
        return dates, date_to_file

    def _delete(self, filename: str) -> None:
        os.remove(filename)

    def creation_date(self, path: str):
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        if platform.system() == 'Windows':
            return os.path.getctime(path)
        else:
            stat = os.stat(path)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return stat.st_mtime