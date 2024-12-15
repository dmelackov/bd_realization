import asyncio
from .database import create_db_and_tables
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from .gui import MyWidget
from bd_realization.constant_tables.table3_5 import fill_table as table1
from bd_realization.constant_tables.table3_6 import fill_table as table2

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] == "fill":
        print("Filling constant tables")
        table1()
        table2()
    create_db_and_tables()
    app = QtWidgets.QApplication([])
    app.setApplicationName("BD Realization")
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())