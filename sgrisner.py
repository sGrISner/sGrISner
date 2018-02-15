#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from lib.vue import MainWindow

import lib.strategy
import lib.model


def main():
    """Affichage de l'interface principale."""

    app = QApplication(sys.argv)
    viewer = MainWindow()
    viewer.show()
    app.exec_()


if __name__ == '__main__':
    main()
