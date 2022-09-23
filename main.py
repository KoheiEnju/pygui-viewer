from collections import deque
from sys import argv
from tkinter import Widget

import cv2
import numpy as np
import PySimpleGUI as sg

from pathlib import Path

if len(argv) == 1:
    print("No arguments")
    exit(1)


def pngbytes(img: np.ndarray) -> bytes:
    data: np.ndarray
    _, data = cv2.imencode(".png", img)
    return data.tobytes()


def resize(img: np.ndarray, maxHeight: int, maxWidth: int) -> np.ndarray:
    height, width = img.shape[:2]
    if height <= maxHeight and width <= maxWidth:
        return img

    ratio = min(maxHeight / height, maxWidth / width)
    img = cv2.resize(img, dsize=None, fx=ratio, fy=ratio)
    return img


img = cv2.imread(argv[1])
size = img.shape[:2]

sg.theme("DefaultNoMoreNagging")
window = sg.Window(
    title=argv[1],
    layout=[[sg.Image(data=pngbytes(img), key="image", size=size)]],
    finalize=True,
    margins=(0, 0),
    icon=None
)
window.bind("<Button-1>", "CLICK")
img_window = window["image"]
img_widget: Widget = img_window.Widget

que = deque()
for i in range(1, len(argv)):
    que.append(argv[i])
que.append(que.popleft())

flg = None
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "CLICK":
        x = (
            img_widget.winfo_pointerx()
            - img_widget.winfo_rootx()
            - img_window.get_size()[0] / 2
        )

        if x >= 0:
            current = que.popleft()
            que.append(current)
            if flg == False:
                current = que.popleft()
                que.append(current)
            flg = True
        else:
            current = que.pop()
            que.appendleft(current)
            if flg == True:
                current = que.pop()
                que.appendleft(current)
            flg = False
        window.set_title(current)
        img = resize(cv2.imread(current), *size)
        img_window.update(data=pngbytes(img), size=size)
