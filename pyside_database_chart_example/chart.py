from typing import List, DefaultDict
from collections import defaultdict
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QSplitter
from PySide6.QtCharts import QChart, QChartView, QBarSet, \
    QBarCategoryAxis, QBarSeries
from PySide6.QtSql import QSqlQuery, QSqlRecord
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter


class ChartWidget(QWidget):
    added = Signal(QSqlRecord)
    deleted = Signal(int)

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle("QtChart Example")

        self.__series = QBarSeries()
        self.__series.hovered.connect(self.__seriesHovered)

        self.__chart = QChart()
        self.__chart.setTitle("Barchart Example")
        self.__chart.setAnimationOptions(QChart.SeriesAnimations)
        self.__chart.setTheme(QChart.ChartThemeDark)
        # self.__chart.setAnimationOptions(QChart.AllAnimations)
        # self.__chart.setAcceptHoverEvents(True)

        self.__axis = QBarCategoryAxis()

        #create chartview and add the pyside_database_chart_example in the chartview
        chartView = QChartView(self.__chart)
        chartView.setRenderHints(QPainter.Antialiasing)

        self.__textBrowser = QTextBrowser()
        self.__textBrowser.setPlaceholderText('Bar series info under the mouser cursor')

        splitter = QSplitter()
        splitter.addWidget(chartView)
        splitter.addWidget(self.__textBrowser)
        splitter.setOrientation(Qt.Vertical)
        splitter.setHandleWidth(1)
        splitter.setSizes([700, 300])
        splitter.setChildrenCollapsible(False)

        lay = QVBoxLayout()
        lay.addWidget(splitter)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

        self.added.connect(self.__add)
        self.deleted.connect(self.__delete)

    def __refreshChart(self):
        self.__chart.addSeries(self.__series)
        self.__chart.createDefaultAxes()
        self.__chart.setAxisX(self.__axis, self.__series)
        self.__axis.remove('Wild Canyon')
        print(self.__axis.min(), self.__axis.max())
        print(self.__axis.count())

    def setDatabase(self):
        selectTableQuery = QSqlQuery()
        attributes = ['city_escape', 'wild_canyon', 'prison_lane']
        selectTableQuery.prepare(f'''
        SELECT name, {attributes[0]}, {attributes[1]}, {attributes[2]} FROM contacts
        ''')
        selectTableQuery.exec()
        name, city_escape, wild_canyon, prison_lane = range(4)
        barsets = []
        columns = defaultdict(list)
        while selectTableQuery.next():
            barset = QBarSet(selectTableQuery.value(name))
            barsets.append(barset)
            columns[attributes[0]].append(selectTableQuery.value(city_escape))
            columns[attributes[1]].append(selectTableQuery.value(wild_canyon))
            columns[attributes[2]].append(selectTableQuery.value(prison_lane))
        self.__axis.append([' '.join(attribute.split('_')).title() for attribute in attributes])
        self.setBarsets(barsets)
        self.setColumnsToBarSet(columns, barsets)
        self.__refreshChart()

    def setBarsets(self, barsets: List[QBarSet]):
        for barset in barsets:
            # barset.hovered.connect(self.__barsetHovered)
            self.__series.append(barset)

    def setColumnsToBarSet(self, columns: DefaultDict[str, List[str]], barsets: List[QBarSet]):
        time_str_to_sec = lambda time_str: sum(x * int(t) for x, t in zip([60, 1], time_str.split(":")))
        for k, v in columns.items():
            time_sec_lst = list(map(time_str_to_sec, v))
            for i in range(len(time_sec_lst)):
                barsets[i] <<= time_sec_lst[i]

    def __add(self, r):
        print(r)
        print('add')

    def __delete(self, id):
        print(f'{id} delete')

    def __seriesHovered(self, status, idx, barset):
        print('__seriesHovered')
        hoveredSeriesInfo = f'''
        On the bar: {status}
        Index of barset: {idx}
        Barset object: {barset}
        Barset object label: {barset.label()}
        Barset object category: {self.__axis.categories()[idx]}
        Barset object value: {barset.at(idx)}
        '''
        self.__textBrowser.setText(hoveredSeriesInfo)

    # def __barsetHovered(self, status, idx):
    #     print('__barsetHovered')
    #     print(f'On the bar: {status}')
    #     print(f'Index of barset: {idx}')
    #     print('')