from __future__ import annotations
from typing import Any


class Sheet():
    name: str
    data: list[list]

    def __init__(self, name) -> None:
        self.name = name
        self._init_data(3, 3)
    
    def __str__(self) -> str:
        return_str = 'Sheet:\n'
        return_str += '\n'.join(map(str, [row for row in self.data]))
        return return_str

    def _init_data(self, rows, cols) -> None:
        self.data = [[0 for c in range(cols)] for r in range(rows)]
        pass

    def edit_sheet(self, row: int, col: int, val: Any) -> None:
        self.data[row][col] = val
    
    def update_data(self, new_sheet: Sheet) -> None:
        self.data = new_sheet.data


class User():
    name: str

    def __init__(self, name: str) -> None:
        self.name = name
