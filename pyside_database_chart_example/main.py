from PySide6.QtWidgets import QMainWindow, QApplication, QSplitter

from pyside_database_chart_example.chart import ChartWidget
from pyside_database_chart_example.db import createConnection, initTable, addSample, DatabaseWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        if not createConnection():
            sys.exit(1)
        initTable()
        addSample()

        db = DatabaseWidget()
        chart = ChartWidget()
        chart.setDatabase(db)

        splitter = QSplitter()
        splitter.addWidget(db)
        splitter.addWidget(chart)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([500, 500])
        splitter.setStyleSheet(
            "QSplitterHandle {background-color: lightgray;}")

        self.setCentralWidget(splitter)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())