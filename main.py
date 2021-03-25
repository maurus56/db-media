from mainWindow import Ui_MainWindow
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import csv


class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.Handle_UI_Changes()
        self.Handle_Buttons()
        self.Handle_Variables()

    def Handle_Variables(self):
        self.file = None

    def Handle_UI_Changes(self):
        self.main_table.setRowCount(0)
        headers = ['id', 'country', 'city', 'name', 'social', 'mail', 'phone', 'nota']
        self.main_table.setColumnCount(len(headers))
        self.add_to_table(data=headers)
    #     self.MainTabs_tabWidget.tabBar().setVisible(False)
    #     # self.Books_tabWidget.tabBar().setVisible(False)
    #     self.Toggle_Themes()
    #     self.currentId = None

    def Handle_Buttons(self):
        self.actionOpen.triggered.connect(self.handleOpen)
        self.actionSave.triggered.connect(self.handleSave)
        self.add_btn.clicked.connect(self.add_to_table)

        # self.Day_To_Day_btn.clicked.connect(self.Open_Day_To_Day_tab)

    ####################################################################
    ################  --------  ########################################
    def add_to_table(self, data: list = None):
        rowPosition = self.main_table.rowCount()
        if not data:
            data = []
            data.append(str(rowPosition))
            data.append(self.country_input.text())
            data.append(self.city_input.text())
            data.append(self.name_input.text())
            data.append(self.social_input.text())
            data.append(self.mail_input.text())
            data.append(self.phone_input.text())
            data.append(self.nota_input.text())
        self.main_table.insertRow(rowPosition)
        for i in range(len(data)):
            self.main_table.setItem(rowPosition, i, QTableWidgetItem(data[i]))
        self.clear_input()

    def clear_input(self):
        self.country_input.clear()
        self.city_input.clear()
        self.name_input.clear()
        self.social_input.clear()
        self.mail_input.clear()
        self.phone_input.clear()
        self.nota_input.clear()

    ####################################################################
    ################  Database  ########################################

    def handleSave(self):
        if not self.file:
            self.file = QFileDialog.getSaveFileName(
                self, 'Save File', '', 'CSV(*.csv)')[0]
        if self.file:
            with open(self.file, '+w') as stream:
                writer = csv.writer(stream)
                for row in range(self.main_table.rowCount()):
                    rowdata = []
                    for column in range(self.main_table.columnCount()):
                        item = self.main_table.item(row, column)
                        if item is not None:
                            rowdata.append(item.text())
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)

    def handleOpen(self):
        path = QFileDialog.getOpenFileName(
            self, caption='Open File', directory='', filter='CSV(*.csv)')
        if path[0]:
            self.file = path[0]
            with open(path[0], 'r') as stream:
                self.main_table.setRowCount(0)
                self.main_table.setColumnCount(0)
                for row, rowdata in enumerate(csv.reader(stream)):
                    self.main_table.insertRow(row)
                    self.main_table.setColumnCount(len(rowdata))
                    for column, data in enumerate(rowdata):
                        item = QTableWidgetItem(data)
                        self.main_table.setItem(row, column, item)

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText(
            "You sure?\n\nPlease save before closing.\nAny unsaved data will be lost.")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
