import os

from PySide6.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery, QSqlRecord
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QStyledItemDelegate, QLabel, QTableView, QAbstractItemView, QPushButton, \
    QHBoxLayout, QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QMessageBox, QComboBox, QGridLayout, QApplication, \
    QLineEdit
from PySide6.QtCore import Qt, QSortFilterProxyModel, Signal


class InstantSearchBar(QWidget):
    searched = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        # search bar label
        self.__label = QLabel()

        self.__searchLineEdit = QLineEdit()
        self.__searchIcon = QSvgWidget()
        ps = QApplication.font().pointSize()
        self.__searchIcon.setFixedSize(ps, ps)

        self.__searchBar = QWidget()
        self.__searchBar.setObjectName('searchBar')

        lay = QHBoxLayout()
        lay.addWidget(self.__searchIcon)
        lay.addWidget(self.__searchLineEdit)
        self.__searchBar.setLayout(lay)
        lay.setContentsMargins(ps // 2, 0, 0, 0)
        lay.setSpacing(0)

        self.__searchLineEdit.setFocus()
        self.__searchLineEdit.textChanged.connect(self.__searched)

        self.setAutoFillBackground(True)

        lay = QHBoxLayout()
        lay.addWidget(self.__searchBar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(2)

        self._topWidget = QWidget()
        self._topWidget.setLayout(lay)

        lay = QGridLayout()
        lay.addWidget(self._topWidget)

        searchWidget = QWidget()
        searchWidget.setLayout(lay)
        lay.setContentsMargins(0, 0, 0, 0)

        lay = QGridLayout()
        lay.addWidget(searchWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        self.__setStyle()

        self.setLayout(lay)

    # ex) searchBar.setLabel(True, 'Search Text')
    def setLabel(self, visibility: bool = True, text=None):
        if text:
            self.__label.setText(text)
        self.__label.setVisible(visibility)

    def __setStyle(self):
        self.__searchIcon.load(os.path.join(os.path.dirname(__file__), 'ico/search.svg'))
        # set style sheet
        with open(os.path.join(os.path.dirname(__file__), 'style/lineedit.css'), 'r') as f:
            self.__searchLineEdit.setStyleSheet(f.read())
        with open(os.path.join(os.path.dirname(__file__), 'style/search_bar.css'), 'r') as f:
            self.__searchBar.setStyleSheet(f.read())
        with open(os.path.join(os.path.dirname(__file__), 'style/widget.css'), 'r') as f:
            self.setStyleSheet(f.read())

    def __searched(self, text):
        self.searched.emit(text)

    def setSearchIcon(self, icon_filename: str):
        self.__searchIcon.load(icon_filename)

    def setPlaceHolder(self, text: str):
        self.__searchLineEdit.setPlaceholderText(text)

    def getSearchBar(self):
        return self.__searchLineEdit

    def getSearchLabel(self):
        return self.__searchIcon

    def showEvent(self, e):
        self.__searchLineEdit.setFocus()


# for search feature
class FilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.__searchedText = ''

    @property
    def searchedText(self):
        return self.__searchedText

    @searchedText.setter
    def searchedText(self, value):
        self.__searchedText = value
        self.invalidateFilter()


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class DatabaseWidget(QWidget):
    added = Signal(QSqlRecord)
    deleted = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle("Qt Database Example")

        # table name
        tableName = "contacts"

        # label
        lbl = QLabel(tableName.capitalize())

        columnNames = ['ID', 'Name', 'Job', 'Email', 'City Escape', 'Wild Canyon', 'Prison Lane']

        # database table
        # set up the model
        self.__tableModel = QSqlTableModel(self)
        self.__tableModel.setTable(tableName)
        self.__tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        for i in range(len(columnNames)):
            self.__tableModel.setHeaderData(i, Qt.Horizontal, columnNames[i])
        self.__tableModel.select()

        # init the proxy model
        self.__proxyModel = FilterProxyModel()

        # set the table model as source model to make it enable to feature sort and filter function
        self.__proxyModel.setSourceModel(self.__tableModel)

        # set up the view
        self.__view = QTableView()
        self.__view.setModel(self.__proxyModel)

        # align to center
        delegate = AlignDelegate()
        for i in range(self.__tableModel.columnCount()):
            self.__view.setItemDelegateForColumn(i, delegate)

        # set selection/resize policy
        self.__view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.__view.resizeColumnsToContents()
        self.__view.setSelectionMode(QAbstractItemView.SingleSelection)

        # sort (ascending order by default)
        self.__view.setSortingEnabled(True)
        self.__view.sortByColumn(0, Qt.AscendingOrder)

        # set current index as first record
        self.__view.setCurrentIndex(self.__view.model().index(0, 0))

        # add/delete buttons
        addBtn = QPushButton('Add')
        addBtn.clicked.connect(self.__add)
        self.__delBtn = QPushButton('Delete')
        self.__delBtn.clicked.connect(self.__delete)

        # instant search bar
        self.__searchBar = InstantSearchBar()
        self.__searchBar.setPlaceHolder('Search...')
        self.__searchBar.searched.connect(self.__showResult)

        # combo box to make it enable to search by each column
        self.__comboBox = QComboBox()
        items = ['All'] + columnNames
        for i in range(len(items)):
            self.__comboBox.addItem(items[i])
        self.__comboBox.currentIndexChanged.connect(self.__currentIndexChanged)

        # set layout
        lay = QHBoxLayout()
        lay.addWidget(lbl)
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(self.__searchBar)
        lay.addWidget(self.__comboBox)
        lay.addWidget(addBtn)
        lay.addWidget(self.__delBtn)
        lay.setContentsMargins(0, 0, 0, 0)
        btnWidget = QWidget()
        btnWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(btnWidget)
        lay.addWidget(self.__view)

        self.setLayout(lay)

        # show default result (which means "show all")
        self.__showResult('')

    def __delBtnToggle(self):
        self.__delBtn.setEnabled(self.__view.model().rowCount() > 0)

    def __add(self):
        r = self.__tableModel.record()
        r.setValue("name", '')
        r.setValue("job", '')
        r.setValue("email", '')
        self.__tableModel.insertRecord(-1, r)
        self.__tableModel.select()
        self.__view.setCurrentIndex(self.__view.model().index(self.__view.model().rowCount() - 1, 0))
        self.added.emit(r)
        self.__view.edit(self.__view.currentIndex().siblingAtColumn(1))
        self.__delBtnToggle()

    def __delete(self):
        r = self.__view.currentIndex().row()
        id = self.__tableModel.index(r, 0).data()
        self.__tableModel.removeRow(r)
        self.__tableModel.select()
        self.__view.setCurrentIndex(self.__view.model().index(max(0, r - 1), 0))
        self.deleted.emit(id)
        self.__delBtnToggle()

    def __showResult(self, text):
        # index -1 will be read from all columns
        # otherwise it will be read the current column number indicated by combobox
        self.__proxyModel.setFilterKeyColumn(self.__comboBox.currentIndex() - 1)
        # regular expression can be used
        self.__proxyModel.setFilterRegularExpression(text)

    def __currentIndexChanged(self, idx):
        self.__showResult(self.__searchBar.getSearchBar().text())


def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("contacts.sqlite")
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True


def initTable():
    table = 'contacts'

    dropTableQuery = QSqlQuery()
    dropTableQuery.prepare(
        f'DROP TABLE {table}'
    )
    dropTableQuery.exec()

    createTableQuery = QSqlQuery()
    createTableQuery.prepare(
        f"""
        CREATE TABLE {table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            job VARCHAR(50),
            email VARCHAR(40) NOT NULL,
            city_escape TIME,
            wild_canyon TIME,
            prison_lane TIME
        )
        """
    )
    createTableQuery.exec()


def addSample():
    table = 'contacts'

    insertDataQuery = QSqlQuery()
    insertDataQuery.prepare(
        f"""
        INSERT INTO {table} (
            name,
            job,
            email,
            city_escape,
            wild_canyon,
            prison_lane
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """
    )

    # Sample data
    data = [
        ("Joe", "Senior Web Developer", "joe@example.com", "2:51", "1:12", "3:15"),
        ("Lara", "Project Manager", "lara@example.com", "3:25", "2:31", "4:27"),
        ("David", "Data Analyst", "david@example.com", "3:41", "7:33", "5:02"),
        ("Jane", "Senior Python Developer", "jane@example.com", "3:10", "2:43", "3:43"),
    ]

    # Use .addBindValue() to insert data
    for name, job, email, city_escape, wild_canyon, prison_lane in data:
        insertDataQuery.addBindValue(name)
        insertDataQuery.addBindValue(job)
        insertDataQuery.addBindValue(email)
        insertDataQuery.addBindValue(city_escape)
        insertDataQuery.addBindValue(wild_canyon)
        insertDataQuery.addBindValue(prison_lane)
        insertDataQuery.exec()