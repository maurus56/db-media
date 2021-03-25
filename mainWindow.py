# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.country_label = QtWidgets.QLabel(self.centralwidget)
        self.country_label.setGeometry(QtCore.QRect(20, 10, 64, 17))
        self.country_label.setObjectName("country_label")
        self.city_label = QtWidgets.QLabel(self.centralwidget)
        self.city_label.setGeometry(QtCore.QRect(20, 60, 64, 17))
        self.city_label.setObjectName("city_label")
        self.mail_label = QtWidgets.QLabel(self.centralwidget)
        self.mail_label.setGeometry(QtCore.QRect(370, 10, 64, 17))
        self.mail_label.setObjectName("mail_label")
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(150, 10, 64, 17))
        self.name_label.setObjectName("name_label")
        self.phone_label = QtWidgets.QLabel(self.centralwidget)
        self.phone_label.setGeometry(QtCore.QRect(370, 60, 64, 17))
        self.phone_label.setObjectName("phone_label")
        self.add_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_btn.setGeometry(QtCore.QRect(640, 80, 83, 25))
        self.add_btn.setObjectName("add_btn")
        self.main_table = QtWidgets.QTableWidget(self.centralwidget)
        self.main_table.setGeometry(QtCore.QRect(10, 120, 781, 431))
        self.main_table.setObjectName("main_table")
        self.main_table.setColumnCount(0)
        self.main_table.setRowCount(0)
        self.social_label = QtWidgets.QLabel(self.centralwidget)
        self.social_label.setGeometry(QtCore.QRect(150, 60, 81, 17))
        self.social_label.setObjectName("social_label")
        self.country_input = QtWidgets.QLineEdit(self.centralwidget)
        self.country_input.setGeometry(QtCore.QRect(10, 30, 113, 25))
        self.country_input.setObjectName("country_input")
        self.city_input = QtWidgets.QLineEdit(self.centralwidget)
        self.city_input.setGeometry(QtCore.QRect(10, 80, 113, 25))
        self.city_input.setObjectName("city_input")
        self.name_input = QtWidgets.QLineEdit(self.centralwidget)
        self.name_input.setGeometry(QtCore.QRect(140, 30, 200, 25))
        self.name_input.setObjectName("name_input")
        self.social_input = QtWidgets.QLineEdit(self.centralwidget)
        self.social_input.setGeometry(QtCore.QRect(140, 80, 200, 25))
        self.social_input.setObjectName("social_input")
        self.mail_input = QtWidgets.QLineEdit(self.centralwidget)
        self.mail_input.setGeometry(QtCore.QRect(360, 30, 200, 25))
        self.mail_input.setObjectName("mail_input")
        self.phone_input = QtWidgets.QLineEdit(self.centralwidget)
        self.phone_input.setGeometry(QtCore.QRect(360, 80, 200, 25))
        self.phone_input.setObjectName("phone_input")
        self.nota_label = QtWidgets.QLabel(self.centralwidget)
        self.nota_label.setGeometry(QtCore.QRect(590, 10, 64, 17))
        self.nota_label.setObjectName("nota_label")
        self.nota_input = QtWidgets.QLineEdit(self.centralwidget)
        self.nota_input.setGeometry(QtCore.QRect(580, 30, 200, 25))
        self.nota_input.setObjectName("nota_input")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFiles = QtWidgets.QMenu(self.menubar)
        self.menuFiles.setObjectName("menuFiles")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFiles.addAction(self.actionOpen)
        self.menuFiles.addSeparator()
        self.menuFiles.addAction(self.actionSave)
        self.menubar.addAction(self.menuFiles.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.country_label.setText(_translate("MainWindow", "Country"))
        self.city_label.setText(_translate("MainWindow", "City"))
        self.mail_label.setText(_translate("MainWindow", "Mail"))
        self.name_label.setText(_translate("MainWindow", "Name"))
        self.phone_label.setText(_translate("MainWindow", "Phone"))
        self.add_btn.setText(_translate("MainWindow", "Add"))
        self.social_label.setText(_translate("MainWindow", "Social"))
        self.nota_label.setText(_translate("MainWindow", "Nota"))
        self.menuFiles.setTitle(_translate("MainWindow", "Files"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
