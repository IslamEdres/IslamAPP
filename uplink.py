from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reports App")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.label = QLabel("Hello, Welcome to the Reports App")
        layout.addWidget(self.label)

        self.create_bar_chart()
        layout.addWidget(self.canvas)

        central_widget.setLayout(layout)

    def create_bar_chart(self):
        years = [2019, 2020, 2021, 2022, 2023]
        europe_data = [510, 620, 687, 745, 881]

        fig, ax = plt.subplots()
        ax.bar(years, europe_data)
        ax.set_title("Bar Chart Example")

        self.canvas = FigureCanvas(fig)

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
