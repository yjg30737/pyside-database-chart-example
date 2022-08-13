from typing import List
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QBarSet, \
    QBarCategoryAxis, QBarSeries


class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle("QtChart Example")

        set0 = QBarSet("Joe")
        set1 = QBarSet("Lara")
        set2 = QBarSet("David")
        set3 = QBarSet("Jane")

        def getTimeList() -> List[List[str]]:
            joe_time_str_lst = ["2:51", "1:12", "3:15"]
            lara_time_str_lst = ["3:25", "2:31", "4:27"]
            david_time_str_lst = ["3:41", "7:33", "5:02"]
            jane_time_str_lst = ["3:10", "2:43", "3:43"]
            lst = [joe_time_str_lst, lara_time_str_lst, david_time_str_lst, jane_time_str_lst]
            return lst

        def setTimeToBarSet(time_str_lst_group: List[List[str]], barset: List[QBarSet]):
            time_str_to_sec = lambda time_str: sum(x * int(t) for x, t in zip([60, 1], time_str.split(":")))
            for i in range(len(time_str_lst_group)):
                time_sec_lst = list(map(time_str_to_sec, time_str_lst_group[i]))
                for time_sec in time_sec_lst:
                    barset[i] <<= time_sec

        time_lst = getTimeList()
        barsets = [set0, set1, set2, set3]
        setTimeToBarSet(time_lst, barsets)

        series = QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Barchart Example")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeDark)

        categories = ["City Escape", "Wild Canyon", "Prison Lane"]

        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        #create chartview and add the pyside_database_chart_example in the chartview
        chartView = QChartView(chart)

        lay = QVBoxLayout()
        lay.addWidget(chartView)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)