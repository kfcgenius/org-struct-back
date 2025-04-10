import os
from abc import ABC, abstractmethod
from csv import reader

from org_struct_back.settings.struct_reader_settings import StructReaderSettings
from org_struct_back.storage.entities import NodeEntity


class StructReader(ABC):
    @abstractmethod
    def parse(self) -> NodeEntity | None:
        pass


class StructReaderImpl(StructReader):
    def __init__(self, settings: StructReaderSettings) -> None:
        self._settings = settings
        self._lines = self._read_csv()

    def parse(self) -> NodeEntity | None:
        return None

    def _read_csv(self) -> list[list[str]]:
        if not os.path.isfile(self._settings.csv_path):
            return []

        with open(self._settings.csv_path, encoding="utf-8") as f:
            return list(reader(f))
