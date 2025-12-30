\
from __future__ import annotations

from typing import Any, Callable, Dict, Tuple

from mysql.connector import Error

from operations.queries import rollback
from utils.utils import prompt


def crud_menu(conn, title: str, handlers: Dict[str, Tuple[str, Callable[[Any], None]]]):
    while True:
        print(f"\n=== {title} ===")
        for k, (label, _) in handlers.items():
            print(f"{k}) {label}")
        choice = prompt("Choose")
        if choice == "0":
            return
        if choice in handlers:
            try:
                handlers[choice][1](conn)
            except Error as e:
                print(f"DB error: {e}")
                rollback(conn)
        else:
            print("Invalid choice.")
