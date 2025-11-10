from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie, QCursor
from PyQt5.QtCore import Qt, QTimer
import sys
import math

app = QApplication(sys.argv)

label = QLabel()
label.setWindowFlags(
    Qt.FramelessWindowHint |
    Qt.WindowStaysOnTopHint |
    Qt.Tool
)
label.setAttribute(Qt.WA_TranslucentBackground)

main_dir = "./assets/"

# Load GIF
movie = QMovie(main_dir + "walk-8.gif")
label.setMovie(movie)
movie.start()

label.adjustSize()

# Init Position
screen = app.primaryScreen().geometry()
label_width = label.width()
label_height = label.height()

x = (screen.width() - label_width) // 2
y = screen.height() - label_height - 50
label.move(x, y)
label.show()

speed = 5  # (1 = lambat, 10 = cepat)

timer = QTimer()

def follow_mouse():
    global x, y
    mouse_pos = QCursor.pos()

    target_x = mouse_pos.x() - label_width // 2
    target_y = mouse_pos.y() - label_height // 2

    dx = target_x - x
    dy = target_y - y
    distance = math.hypot(dx, dy)

    if distance < 1:
        return

    dir_x = dx / distance
    dir_y = dy / distance

    x += dir_x * speed
    y += dir_y * speed

    label.move(int(x), int(y))

timer.timeout.connect(follow_mouse)
timer.start(16)  # 60 FPS

sys.exit(app.exec_())
