import sys
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class PomodoroTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")
        self.setGeometry(200, 200, 300, 200)

        # Timer durations
        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.time_left = self.work_duration
        self.is_work_session = True
        self.timer_running = False

        # UI Elements
        self.timer_label = QLabel("25:00", self)
        self.timer_label.setStyleSheet('font-size: 32px; font-weight: bold;')
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.toggle_timer)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_timer)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.reset_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def toggle_timer(self):
        if self.timer_running:
            self.timer.stop()
            self.start_button.setText("Start")
        else:
            self.timer.start(1000)  # Update every second
            self.start_button.setText("Pause")
        self.timer_running = not self.timer_running

    def reset_timer(self):
        self.timer.stop()
        self.time_left = self.work_duration if self.is_work_session else self.break_duration
        self.timer_running = False
        self.start_button.setText("Start")
        self.update_timer_label()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_label()
        else:
            self.timer.stop()
            self.timer_running = False
            self.start_button.setText("Start")
            self.is_work_session = not self.is_work_session
            self.time_left = self.break_duration if not self.is_work_session else self.work_duration
            self.update_timer_label()

    def update_timer_label(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PomodoroTimer()
    window.show()
    sys.exit(app.exec_())
