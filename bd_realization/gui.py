import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui, QtAsyncio
from .logic import generate_default, calculate, save_values
from .models import Node, AssemblyUnit, Part

current_node: Node | None = None
current_assembly_unit: AssemblyUnit | None = None
current_belt: Part | None = None
current_shift_1: Part | None = None
current_shift_2: Part | None = None


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.widget_classes = [StartWidget,  NodeWidget, AssemblyUnitWidget, Part1Widget,
                               Part2Widget, Part3Widget, ResultWidget]
        self.current_stage = 0
        self.current_widget = None

        self.inner_layout = QtWidgets.QVBoxLayout(self)
        self.inner_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.load_stage()

    def load_stage(self):
        print("loading stage", self.current_stage)
        if self.current_widget is not None:
            self.inner_layout.removeWidget(self.current_widget)
            self.current_widget.deleteLater()
        self.current_widget = self.widget_classes[self.current_stage]()
        print("loaded", type(self.current_widget))
        self.inner_layout.addWidget(self.current_widget)
        self.current_widget.next_signal.connect(self.load_next_stage)

    @QtCore.Slot()
    def load_next_stage(self):
        self.current_stage += 1
        if self.current_stage >= len(self.widget_classes):
            self.current_stage = 0
        self.load_stage()


class StartWidget(QtWidgets.QWidget):
    next_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Начать проектировочный расчет")
        self.button.clicked.connect(self.start)

        self.inner_layout = QtWidgets.QVBoxLayout(self)
        self.inner_layout.addWidget(self.button)

    @QtCore.Slot()
    def start(self):
        global current_node, current_assembly_unit, current_belt, current_shift_1, current_shift_2
        current_node, current_assembly_unit, current_belt, current_shift_1, current_shift_2 = generate_default()
        self.next_signal.emit()


class NodeWidget(QtWidgets.QWidget):
    next_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        if current_node is None:
            return

        available_machine = [
            "Деревообрабатывающее оборудование",
            "Токарные станки и оборудование для типографии",
            "Сверлильные, расточные, шлифовальные, фрезерные, поперечно-строгальные и долбежные станки",
            "Конвейеры ленточные",
            "Вентиляторы, подъемники и текстильное оборудование",
            "Пластинчатый, ковшовый и элеваторный конвейеры",
            "Скребковый и шнековый конвейер"
        ]

        available_mode = [
            "Двухсменный",
            "Трехсменный"
        ]

        self.inner_layout = QtWidgets.QVBoxLayout(self)
        self.inner_layout.addWidget(QtWidgets.QLabel("Введите параметры узла"))
        self.machine_mode = QtWidgets.QComboBox()
        self.machine_mode.addItems(available_machine)
        if current_node.machine_mode is not None:
            self.machine_mode.setCurrentText(current_node.machine_mode)

        self.shift_mode = QtWidgets.QComboBox()
        self.shift_mode.addItems(available_mode)
        if current_node.shift_mode is not None:
            self.shift_mode.setCurrentText(current_node.shift_mode)

        self.inner_layout.addWidget(QtWidgets.QLabel("Тип оборудования:"))
        self.inner_layout.addWidget(self.machine_mode)
        self.inner_layout.addWidget(QtWidgets.QLabel("Режим работы:"))
        self.inner_layout.addWidget(self.shift_mode)
        self.button = QtWidgets.QPushButton("Следующий шаг")
        self.button.clicked.connect(self.next)
        self.inner_layout.addWidget(self.button)

    @QtCore.Slot()
    def next(self):
        if current_node is None:
            return
        current_node.machine_mode = self.machine_mode.currentText()
        current_node.shift_mode = self.shift_mode.currentText()
        self.next_signal.emit()


class AssemblyUnitWidget(QtWidgets.QWidget):
    next_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        if current_assembly_unit is None:
            return

        self.inner_layout = QtWidgets.QVBoxLayout(self)
        

        self.inner_layout.addWidget(QtWidgets.QLabel(
            f"Наименование: {current_assembly_unit.NSE}"))
        self.inner_layout.addWidget(QtWidgets.QLabel(
            f"Тип: {current_assembly_unit.TSE}"))
        self.inner_layout.addWidget(QtWidgets.QLabel(
            f"Вид: {current_assembly_unit.VSE}"))
        self.inner_layout.addWidget(QtWidgets.QLabel(
            "Введите параметры сборочной единицы"))
        self.F = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Рабочая нагрузка, F:"))
        self.inner_layout.addWidget(self.F)
        self.peak_load = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Максимальная пиковая нагрузка, peak_load:"))
        self.inner_layout.addWidget(self.peak_load)
        self.t_ch = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Общее время работы передачи, t_ch:"))
        self.inner_layout.addWidget(self.t_ch)
        self.F1 = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Максимально длительно действующая нагрузка, F1:"))
        self.inner_layout.addWidget(self.F1)
        self.j = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Число режимов работы, j:"))
        self.inner_layout.addWidget(self.j)
        self.F_j = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Нагрузка при режиме j, F_j:"))
        self.inner_layout.addWidget(self.F_j)
        self.t_ch_j = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Время работы при режиме j, t_ch_j:"))
        self.inner_layout.addWidget(self.t_ch_j)
        self.a = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Расстояние между осями шкива, a:"))
        self.inner_layout.addWidget(self.a)
        self.working_mode = QtWidgets.QComboBox()
        self.working_mode.addItems(["Постоянный", "Переменный"])
        self.inner_layout.addWidget(QtWidgets.QLabel("Режим работы:"))
        self.inner_layout.addWidget(self.working_mode)
        self.roller_count = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Количество роликов, roller_count:"))
        self.inner_layout.addWidget(self.roller_count)


        self.button = QtWidgets.QPushButton("Следующий шаг")
        self.button.clicked.connect(self.next)
        self.inner_layout.addWidget(self.button)

    @QtCore.Slot()
    def next(self):
        if current_assembly_unit is None:
            return
        current_assembly_unit.F = float(self.F.text())
        current_assembly_unit.peak_load = float(self.peak_load.text())
        current_assembly_unit.t_ch = float(self.t_ch.text())
        current_assembly_unit.F1 = float(self.F1.text())
        current_assembly_unit.j = int(self.j.text())
        current_assembly_unit.F_j = float(self.F_j.text())
        current_assembly_unit.t_ch_j = float(self.t_ch_j.text())
        current_assembly_unit.a = float(self.a.text())
        current_assembly_unit.working_mode = self.working_mode.currentText()
        current_assembly_unit.roller_count = int(self.roller_count.text())
        self.next_signal.emit()


class Part1Widget(QtWidgets.QWidget):
    next_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        if current_belt is None:
            return
        
        self.inner_layout = QtWidgets.QVBoxLayout(self)

        self.inner_layout.addWidget(QtWidgets.QLabel(f"Наименование: {current_belt.ND}"))
        self.inner_layout.addWidget(QtWidgets.QLabel("Введите данные детали"))

        self.b = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Ширина ремня, b:"))
        self.inner_layout.addWidget(self.b)
        
        self.rubber_mark = QtWidgets.QComboBox()
        self.rubber_mark.addItems(["В-14", "В-14-2", "ИРП1078", "НО-68-1"])
        self.inner_layout.addWidget(QtWidgets.QLabel("Марка резины, rubber_mark:"))
        self.inner_layout.addWidget(self.rubber_mark)
        
        self.z_p = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Число зубьев ремня, z_p:"))
        self.inner_layout.addWidget(self.z_p)
        
        self.m = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Модуль ремня, m:"))
        self.inner_layout.addWidget(self.m)
        
        self.cable_type = QtWidgets.QComboBox()
        self.cable_type.addItems(["1x7", "1x21"])
        self.inner_layout.addWidget(QtWidgets.QLabel("Тип троса, cable_type:"))
        self.inner_layout.addWidget(self.cable_type)

        self.S = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Наименьшая толщина зуба, S:"))
        self.inner_layout.addWidget(self.S)
        
        
        self.button = QtWidgets.QPushButton("Следующий шаг")
        self.button.clicked.connect(self.next)
        self.inner_layout.addWidget(self.button)

    @QtCore.Slot()
    def next(self):
        if current_belt is None:
            return
        current_belt.b = float(self.b.text())
        current_belt.rubber_mark = self.rubber_mark.currentText()
        current_belt.z_p = int(self.z_p.text())
        current_belt.m = float(self.m.text())
        current_belt.cable_type = self.cable_type.currentText()
        current_belt.S = float(self.S.text())
        self.next_signal.emit()

class Part2Widget(QtWidgets.QWidget):
    next_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        if current_shift_1 is None:
            return
        
        self.inner_layout = QtWidgets.QVBoxLayout(self)

        self.inner_layout.addWidget(QtWidgets.QLabel(f"Наименование: {current_shift_1.ND}"))
        self.inner_layout.addWidget(QtWidgets.QLabel(f"Назначение: {current_shift_1.NAD}"))
        self.inner_layout.addWidget(QtWidgets.QLabel("Введите параметры шкива"))

        self.z1 = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Число зубьев малого шкива, z1:"))
        self.inner_layout.addWidget(self.z1)

        self.n1 = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Частота вращения малого шкива, n1:"))
        self.inner_layout.addWidget(self.n1)

        self.n_j = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Частота вращения шкива при режиме j, n_j:"))
        self.inner_layout.addWidget(self.n_j)

        self.gamma = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Угол впадины, gamma:"))
        self.inner_layout.addWidget(self.gamma)

        self.d_a1 = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Диаметр вершин зубьев малого шкива, d_a1:"))
        self.inner_layout.addWidget(self.d_a1)

        self.h = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Высота зуба, h:"))
        self.inner_layout.addWidget(self.h)

        self.button = QtWidgets.QPushButton("Следующий шаг")
        self.button.clicked.connect(self.next)
        self.inner_layout.addWidget(self.button)

    @QtCore.Slot()
    def next(self):
        if current_shift_1 is None:
            return
        current_shift_1.z1 = int(self.z1.text())
        current_shift_1.n1 = float(self.n1.text())
        current_shift_1.n_j = float(self.n_j.text())
        current_shift_1.gamma = float(self.gamma.text())
        current_shift_1.d_a1 = float(self.d_a1.text())
        current_shift_1.h = float(self.h.text())
        self.next_signal.emit()

class Part3Widget(QtWidgets.QWidget):
    next_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        if current_shift_2 is None:
            return
        
        self.inner_layout = QtWidgets.QVBoxLayout(self)

        self.inner_layout.addWidget(QtWidgets.QLabel(f"Наименование: {current_shift_2.ND}"))
        self.inner_layout.addWidget(QtWidgets.QLabel(f"Назначение: {current_shift_2.NAD}"))
        self.inner_layout.addWidget(QtWidgets.QLabel("Введите параметры шкива"))

        self.z2 = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(QtWidgets.QLabel("Число зубьев большего шкива, z2:"))
        self.inner_layout.addWidget(self.z2)

        self.button = QtWidgets.QPushButton("Следующий шаг")
        self.button.clicked.connect(self.next)
        self.inner_layout.addWidget(self.button)

    @QtCore.Slot()
    def next(self):
        if current_shift_2 is None:
            return
        current_shift_2.z2 = int(self.z2.text())
        calculate(current_node, current_assembly_unit, current_belt, current_shift_1, current_shift_2)  # type: ignore
        self.next_signal.emit()

class ResultWidget(QtWidgets.QWidget):
    next_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.inner_layout = QtWidgets.QVBoxLayout(self)

        self.inner_layout.addWidget(QtWidgets.QLabel(f"Результат условия прочности: {current_assembly_unit.status1 if current_assembly_unit else ''}"))
        self.inner_layout.addWidget(QtWidgets.QLabel(f"Результат условия зацепления: {current_assembly_unit.status2 if current_assembly_unit else ''}"))
        self.inner_layout.addWidget(QtWidgets.QLabel(f"Результат натяжения: {current_belt.Q0 if current_belt else ''}"))

        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save)
        self.inner_layout.addWidget(self.save_button)

        self.cancel_button = QtWidgets.QPushButton("Отменить")
        self.cancel_button.clicked.connect(self.cancel)
        self.inner_layout.addWidget(self.cancel_button)

    @QtCore.Slot()
    def save(self):
        if current_node is None or current_assembly_unit is None or current_belt is None or current_shift_1 is None or current_shift_2 is None:
            return
        save_values(current_node, current_assembly_unit, current_belt, current_shift_1, current_shift_2)
        self.next_signal.emit()

    @QtCore.Slot()
    def cancel(self):
        self.next_signal.emit()

