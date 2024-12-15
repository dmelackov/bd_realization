from bd_realization.constant_tables.table3_6 import get_by_peak_load_and_machine_type
from .models import Node, AssemblyUnit, Part
from .database import sessionmanager

def generate_default() -> tuple[Node, AssemblyUnit, Part, Part, Part]:
    n = Node(id=1)

    a = AssemblyUnit(id=1)
    a.node_id = n.id
    a.NSE = "передача"
    a.TSE = "ременная"
    a.VSE = "с зубчатым ремнем"

    p1 = Part(id=1)
    p1.assembly_unit_id = a.id
    p1.ND = "ремень"

    p2 = Part(id=2)
    p2.assembly_unit_id = a.id
    p2.ND = "шкив"
    p2.NAD = "ведущий"

    p3 = Part(id=3)
    p3.assembly_unit_id = a.id
    p3.ND = "шкив"
    p3.NAD = "ведомый"

    return n, a, p1, p2, p3

def calculate(n: Node, a: AssemblyUnit, p1: Part, p2: Part, p3: Part) -> None:
    a.K_d = get_by_peak_load_and_machine_type(a.peak_load, n.machine_mode) # type: ignore
    p1.alpha1 = 180 - (p1.m * (p3.z2 - p2.z1) / p1.a) * 57.3 # type: ignore
    p2.z0 = p2.z1 * p1.alpha1 / 360 # type: ignore

def save_values(n: Node, a: AssemblyUnit, p1: Part, p2: Part, p3: Part) -> None:
    with sessionmanager.session() as session:
        session.add(n)
        session.add(a)
        session.add(p1)
        session.add(p2)
        session.add(p3)
        session.flush()