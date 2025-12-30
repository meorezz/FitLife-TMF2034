from __future__ import annotations
from datetime import datetime
from typing import Any, Optional, Sequence, Tuple
from prettytable import PrettyTable


def print_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> None:
    t = PrettyTable()
    t.field_names = list(headers)
    for r in rows:
        t.add_row(list(r))
    print(t)


def prompt(msg: str, default: Optional[str] = None) -> str:
    if default is None:
        return input(f"{msg}: ").strip()
    s = input(f"{msg} [{default}]: ").strip()
    return s if s else default


def prompt_int(msg: str, default: Optional[int] = None) -> int:
    while True:
        try:
            val = prompt(msg, str(default) if default is not None else None)
            return int(val)
        except ValueError:
            print("Please enter an integer.")


def prompt_decimal(msg: str, default: Optional[float] = None) -> float:
    while True:
        try:
            val = prompt(msg, str(default) if default is not None else None)
            return float(val)
        except ValueError:
            print("Please enter a number (e.g., 350.00).")


def prompt_datetime(msg: str, default: Optional[str] = None) -> str:
    """
    Accepts 'YYYY-MM-DD HH:MM:SS'
    """
    while True:
        val = prompt(msg, default)
        try:
            datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
            return val
        except ValueError:
            print("Invalid datetime. Format must be: YYYY-MM-DD HH:MM:SS")
