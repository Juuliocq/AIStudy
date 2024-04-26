import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton

from problema_mochila.otimizador.AlgoritmoOtimizador import AlgoritmoOtimizador
from problema_mochila.problema.Algoritmo import Algoritmo


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("mainWindow")
        self.resize(701, 356)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.txt_massa_1 = QLineEdit(self.centralwidget)
        self.txt_massa_1.setObjectName("txt_massa_1")
        self.txt_massa_1.setGeometry(QRect(90, 10, 113, 20))

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(10, 10, 81, 16))

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(210, 10, 81, 16))

        self.txt_valor_1 = QLineEdit(self.centralwidget)
        self.txt_valor_1.setObjectName("txt_valor_1")
        self.txt_valor_1.setGeometry(QRect(290, 10, 113, 20))

        self.txt_qtdlimite_1 = QLineEdit(self.centralwidget)
        self.txt_qtdlimite_1.setObjectName("txt_qtdlimite_1")
        self.txt_qtdlimite_1.setGeometry(QRect(540, 10, 113, 20))

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.label_3.setGeometry(QRect(410, 10, 131, 16))

        self.txt_valor_2 = QLineEdit(self.centralwidget)
        self.txt_valor_2.setObjectName("txt_valor_2")
        self.txt_valor_2.setGeometry(QRect(290, 50, 113, 20))

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.label_4.setGeometry(QRect(210, 50, 81, 16))

        self.txt_qtdlimite_2 = QLineEdit(self.centralwidget)
        self.txt_qtdlimite_2.setObjectName("txt_qtdlimite_2")
        self.txt_qtdlimite_2.setGeometry(QRect(540, 50, 113, 20))

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.label_5.setGeometry(QRect(410, 50, 131, 16))

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.label_6.setGeometry(QRect(10, 50, 81, 16))

        self.txt_massa_2 = QLineEdit(self.centralwidget)
        self.txt_massa_2.setObjectName("txt_massa_2")
        self.txt_massa_2.setGeometry(QRect(90, 50, 113, 20))

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.label_7.setGeometry(QRect(210, 90, 81, 16))

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.label_8.setGeometry(QRect(410, 90, 131, 16))

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.label_9.setGeometry(QRect(10, 90, 81, 16))

        self.txt_qtdlimite_3 = QLineEdit(self.centralwidget)
        self.txt_qtdlimite_3.setObjectName("txt_qtdlimite_3")
        self.txt_qtdlimite_3.setGeometry(QRect(540, 90, 113, 20))

        self.txt_massa_3 = QLineEdit(self.centralwidget)
        self.txt_massa_3.setObjectName("txt_massa_3")
        self.txt_massa_3.setGeometry(QRect(90, 90, 113, 20))

        self.txt_valor_3 = QLineEdit(self.centralwidget)
        self.txt_valor_3.setObjectName("txt_valor_3")
        self.txt_valor_3.setGeometry(QRect(290, 90, 113, 20))

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")
        self.label_10.setGeometry(QRect(10, 130, 81, 16))

        self.txt_limite_massa = QLineEdit(self.centralwidget)
        self.txt_limite_massa.setObjectName("txt_limite_massa")
        self.txt_limite_massa.setGeometry(QRect(100, 130, 113, 20))

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.label_11.setGeometry(QRect(10, 170, 111, 16))

        self.txt_convergencia = QLineEdit(self.centralwidget)
        self.txt_convergencia.setObjectName("txt_convergencia")
        self.txt_convergencia.setGeometry(QRect(130, 170, 113, 20))

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.label_12.setGeometry(QRect(10, 210, 111, 16))

        self.txt_populacao = QLineEdit(self.centralwidget)
        self.txt_populacao.setObjectName("txt_populacao")
        self.txt_populacao.setGeometry(QRect(130, 210, 113, 20))

        self.btn_iniciar = QPushButton(self.centralwidget)
        self.btn_iniciar.setObjectName("btn_iniciar")
        self.btn_iniciar.setGeometry(QRect(310, 290, 75, 23))
        self.btn_iniciar.clicked.connect(self.iniciar)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 475, 21))
        self.menubar.setObjectName("menubar")

        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(_translate("MainWindow", "Algoritmo Genético"))
        self.label.setText(_translate("MainWindow", "Item 1 Massa:", None))
        self.label_2.setText(_translate("MainWindow", "Item 1 Valor:", None))
        self.txt_qtdlimite_1.setText("")
        self.label_3.setText(_translate("MainWindow", "Item 1 Quantidade Limite:", None))
        self.label_4.setText(_translate("MainWindow", "Item 2 Valor:", None))
        self.txt_qtdlimite_2.setText("")
        self.label_5.setText(_translate("MainWindow", "Item 2 Quantidade Limite:", None))
        self.label_6.setText(_translate("MainWindow", "Item 2 Massa:", None))
        self.label_7.setText(_translate("MainWindow", "Item 3 Valor:", None))
        self.label_8.setText(_translate("MainWindow", "Item 3 Quantidade Limite:", None))
        self.label_9.setText(_translate("MainWindow", "Item 3 Massa:", None))
        self.txt_qtdlimite_3.setText("")
        self.label_10.setText(_translate("MainWindow", "Limite de Massa:", None))
        self.label_11.setText(_translate("MainWindow", "Converg\u00eancia m\u00e1xima:", None))
        self.label_12.setText(_translate("MainWindow", "Popula\u00e7\u00e3o m\u00e1xima:", None))
        self.btn_iniciar.setText(_translate("MainWindow", "Iniciar", None))
    # retranslateUi

    def iniciar(self):
        algoritmo = AlgoritmoOtimizador(self.txt_limite_massa.text(), self.txt_populacao.text(),
                              self.txt_convergencia.text(),
                              self.txt_massa_1.text(), self.txt_valor_1.text(), self.txt_qtdlimite_1.text(),
                                self.txt_massa_2.text(), self.txt_valor_2.text(), self.txt_qtdlimite_2.text(),
                                self.txt_massa_3.text(), self.txt_valor_3.text(), self.txt_qtdlimite_3.text())
        algoritmo.iniciar()


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
