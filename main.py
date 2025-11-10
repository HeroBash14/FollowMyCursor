from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie, QCursor
from PyQt5.QtCore import Qt, QTimer
import sys
import math
import os

app = QApplication(sys.argv)

label = QLabel()
label.setWindowFlags(
    Qt.FramelessWindowHint |
    Qt.WindowStaysOnTopHint |
    Qt.Tool
)
label.setAttribute(Qt.WA_TranslucentBackground)

main_dir = "./assets/"
current_dir = 8  # default arah: bawah
speed = 5  # pixel per frame
stop_threshold = 6  # jarak di bawah ini dianggap "diam"
pause_when_idle = True  # jika True, hentikan animasi ketika diam

movie = None

def set_direction(dir_num):
    global current_dir, movie, label, label_width, label_height
    if dir_num == current_dir:
        return
    current_dir = dir_num

    path = os.path.join(main_dir, f"walk-{dir_num}.gif")
    if os.path.exists(path):
        # ganti movie
        if movie is not None:
            movie.stop()
        movie = QMovie(path)
        label.setMovie(movie)
        movie.start()
        label.adjustSize()
        # update ukuran label setelah ganti GIF
        label_width = label.width()
        label_height = label.height()

# === Load initial GIF ===
movie = QMovie(os.path.join(main_dir, f"walk-{current_dir}.gif"))
label.setMovie(movie)
movie.start()
label.adjustSize()

# ukuran awal (akan diupdate kalau ganti GIF)
label_width = label.width()
label_height = label.height()

# === Posisi awal ===
screen = app.primaryScreen().geometry()
x = (screen.width() - label_width) // 2
y = screen.height() - label_height - 50
label.move(x, y)
label.show()

timer = QTimer()

def follow_mouse():
    global x, y, label_width, label_height, movie

    mouse_pos = QCursor.pos()
    target_x = mouse_pos.x() - label_width // 2
    target_y = mouse_pos.y() - label_height // 2

    dx = target_x - x
    dy = target_y - y
    distance = math.hypot(dx, dy)

    # Jika sangat dekat, anggap diam
    if distance < stop_threshold:
        if pause_when_idle and movie is not None and movie.state() == QMovie.Running:
            movie.stop()
        return

    # Pastikan animasi jalan ketika bergerak
    if pause_when_idle and movie is not None and movie.state() != QMovie.Running:
        movie.start()

    # Hitung sudut berdasarkan (dy, dx) — karena y meningkat ke bawah di layar
    angle = math.degrees(math.atan2(dy, dx))  # 0 = right, 90 = down, 180 = left, -90 = up
    angle = (angle + 360) % 360  # 0..360

    # Map sudut ke nomor GIF (sesuai penomoran kamu)
    # 6 = Right, 7 = Down Right, 8 = Down, 1 = Down Left, 2 = Left,
    # 3 = Up Left, 4 = Up, 5 = Up Right
    if 337.5 <= angle or angle < 22.5:
        dir_num = 6  # Right
    elif 22.5 <= angle < 67.5:
        dir_num = 7  # Down Right
    elif 67.5 <= angle < 112.5:
        dir_num = 8  # Down
    elif 112.5 <= angle < 157.5:
        dir_num = 1  # Down Left
    elif 157.5 <= angle < 202.5:
        dir_num = 2  # Left
    elif 202.5 <= angle < 247.5:
        dir_num = 3  # Up Left
    elif 247.5 <= angle < 292.5:
        dir_num = 4  # Up
    elif 292.5 <= angle < 337.5:
        dir_num = 5  # Up Right
    else:
        dir_num = current_dir

    set_direction(dir_num)

    # Gerak dengan kecepatan konstan menuju target
    dir_x = dx / distance
    dir_y = dy / distance

    x += dir_x * speed
    y += dir_y * speed
    label.move(int(x), int(y))


timer.timeout.connect(follow_mouse)
timer.start(30)

sys.exit(app.exec_())
