# pyside-database-chart-example
Example of using database and chart with PySide6

I used PySide6 unlike the others because PyQt5 or PyQt6 is very finicky to import QChart for some reasons.

Note: Data in chart are hard-coded, which means they are not programmatically synchronized with data in database. I will deal with it sooner or later.

You can see the basic description to use the database GUI here - <a href="https://github.com/yjg30737/pyqt-database-example">pyqt-database-example</a>. Yes, it is PyQt database but PySide and PyQt are almost identical so there is not a bit of a problem to understand. 

## Requirements
* PySide6

## Setup
`python -m pip install git+https://github.com/yjg30737/pyside-database-chart-example.git --upgrade`

## Example
```python
from PySide6.QtWidgets import QApplication
from pyside_database_chart_example.main import Window


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
```

Result

![image](https://user-images.githubusercontent.com/55078043/184469977-8dc68ed2-6b76-47e1-8763-b430549392a4.png)
