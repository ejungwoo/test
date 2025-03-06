#!/usr/bin/env python
# coding: utf-8

# 예제 내용
# * 기본 위젯을 사용하여 기본 창을 생성
# * 다양한 레이아웃 위젯 사용

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QCoreApplication, QMimeData
from PyQt5.QtGui import QDrag


class button_exit(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.pressed.connect(self._pressed())#QCoreApplication.instance().quit())
    #def mousePressEvent(self, e):
    #    super().mousePressEvent(e)
    #    if e.button() == Qt.LeftButton:
    def _pressed(self):
        QCoreApplication.instance().quit()

class Button(QPushButton):
    def __init__(self, title, parent): super().__init__(title, parent)

    #def mousePressEvent(self, e):
    #    super().mousePressEvent(e)
    #    if e.button() == Qt.LeftButton:
    def _pressed(self):
         parent.print()

class reference_manager(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)

        self.setWindowTitle("Various Layout Widgets")
        self.setFixedWidth(800)
        self.setFixedHeight(500)

        layout_base = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.setLayout(layout_base)

        #
        group1 = QGroupBox("Actions")
        layout_base.addWidget(group1)
        layout = QHBoxLayout()
        layout.addWidget(Button("Approve",self))
        layout.addWidget(Button("Clear",self))
        layout.addWidget(button_exit("Exit",self))
        group1.setLayout(layout)

        #
        group2 = QGroupBox("Info.")
        layout_base.addWidget(group2)
        grp_2_layout = QBoxLayout(QBoxLayout.LeftToRight)
        group2.setLayout(grp_2_layout)
        layout = QGridLayout()
        layout.addItem(QSpacerItem(10, 100))
        layout.addWidget(QLabel("Line Edit 1:"), 1, 0)
        layout.addWidget(QLabel("Line Edit 2:"), 2, 0)
        layout.addWidget(QLabel("Line Edit 2:"), 3, 0)
        layout.addWidget(QLineEdit(), 1, 1)
        layout.addWidget(QLineEdit(), 2, 1)
        layout.addWidget(QLineEdit(), 3, 1)
        grp_2_layout.addLayout(layout)
        grp_2_layout.addWidget(QTextEdit())

        #
        grp_3 = QGroupBox("Message")
        layout_base.addWidget(grp_3)
        layout = QFormLayout()
        grp_3.setLayout(layout)
        layout.addRow(QLabel("Line Edit 1:"), QLineEdit())
        layout.addRow(QLabel("Line Edit 2:"), QLineEdit())
        layout.addRow(QLabel("Line Edit 3:"), QLineEdit())

    def a(self):
        print("a")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = reference_manager()
    form.show()
    exit(app.exec_())
