from __future__ import annotations

import tkinter as tk

from .model import Map
from .projection import Camera

BG = "#101830"
COLOR_DEFAULT = "#FFFFFF" #"#4682B4"


def _edge_color(a: str | None, b: str | None) -> str:
    return a or b or COLOR_DEFAULT


class App:
    def __init__(self, map_: Map, title: str = "FdF") -> None:
        self.map = map_
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("1000x700")
        self.canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.camera = Camera()
        self.root.bind("<Escape>", lambda _e: self.root.destroy())
        self.canvas.bind("<Configure>", lambda _e: self.redraw())

    def redraw(self) -> None:
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            return
        self.camera.fit(self.map, w, h)
        self.canvas.delete("all")
        for y in range(self.map.height):
            for x in range(self.map.width):
                p = self.map.point(y, x)
                px, py = self.camera.apply(p)
                for n in self.map.neighbors(y, x):
                    nx, ny = self.camera.apply(n)
                    self.canvas.create_line(
                        px, py, nx, ny,
                        fill=_edge_color(p.color, n.color), width=1,
                    )

    def run(self) -> None:
        self.root.mainloop()