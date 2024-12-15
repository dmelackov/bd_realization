import math
from webbrowser import get
from bd_realization.constant_tables.table3_5 import get_by_m_and_cable_type, get_by_rubber_mark
from bd_realization.constant_tables.table3_6 import get_by_peak_load_and_machine_type
from .models import Node, AssemblyUnit, Part
from .database import sessionmanager

def generate_default() -> tuple[Node, AssemblyUnit, Part, Part, Part]:
    with sessionmanager.session() as session:
        stmt = session.query(Node).order_by(Node.id.desc()).first()
        if stmt is None:
            n_id = 0
        else:
            n_id = stmt.id
        n = Node(id=n_id + 1)
        
        stmt = session.query(AssemblyUnit).order_by(AssemblyUnit.id.desc()).first()
        if stmt is None:
            a_id = 0
        else:
            a_id = stmt.id

        a = AssemblyUnit(id=a_id+1)
        a.node_id = n.id
        a.NSE = "передача"
        a.TSE = "ременная"
        a.VSE = "с зубчатым ремнем"

        p1 = Part()
        p1.assembly_unit_id = a.id
        p1.ND = "ремень"

        p2 = Part()
        p2.assembly_unit_id = a.id
        p2.ND = "шкив"
        p2.NAD = "ведущий"

        p3 = Part()
        p3.assembly_unit_id = a.id
        p3.ND = "шкив"
        p3.NAD = "ведомый"

        return n, a, p1, p2, p3

def calculate(n: Node, a: AssemblyUnit, p1: Part, p2: Part, p3: Part) -> None:
    a.K_d = get_by_peak_load_and_machine_type(a.peak_load, n.machine_mode).K_d # type: ignore
    p1.alpha1 = 180 - (p1.m * (p3.z2 - p2.z1) / a.a) * 57.3 # type: ignore
    p2.z0 = p2.z1 * p1.alpha1 / 360 # type: ignore
    p1.S1 = 0.5 * (p1.S + 2 * p2.h * math.tan(p2.gamma)) # type: ignore
    p1.sigma_sd = a.F * a.K_d / (p2.z0 * p1.S1 * p1.b * 2.65) # type: ignore
    if a.working_mode == "Переменный": # type: ignore
        a.N_c = 60 * (p2.z1 / p1.z_p) * a.t_ch / p2.n1 # type: ignore
    if a.working_mode == "Постоянный": # type: ignore
        a.N_c = 60 * (p2.z1 / p1.z_p) * (a.t_ch_j * p2.n_j * (a.F_j / a.F1) ** 6) # type: ignore
    if a.working_mode == "Переменный": # type: ignore
        a.phi_t = (p2.n1 / 10**3) ** (1/6) # type: ignore
    if a.working_mode == "Постоянный": # type: ignore
        a.phi_t = (1 / a.t_ch) * (a.t_ch_j * (p2.n_j / 10**3) ** (1/6)) # type: ignore
    if n.shift_mode == "Двухсменный":
        a.phi_c = 1.07
    if n.shift_mode == "Трехсменный":
        a.phi_c = 1.15
    if a.roller_count == 1:
        a.phi_p = 1.1
    if a.roller_count == 2:
        a.phi_p = 1.25
    a.phi = a.phi_t * a.phi_c * a.phi_p # type: ignore
    a.K_p = a.phi * (a.N_c ** (1/6)) # type: ignore
    p1.sigma_v_s = get_by_rubber_mark(p1.rubber_mark).sigma_v_s # type: ignore
    p1.sigma_sd_ = p1.sigma_sd * 0.8 # type: ignore
    p1.sigma_sd_dop = p1.sigma_sd_ / a.K_p  # type: ignore
    p1.sigma_sd_diff = p1.sigma_sd_dop - p1.sigma_sd # type: ignore
    a.status1 = 'Выполняется' if p1.sigma_sd_diff > 0 else 'Не выполняется' # type: ignore

def save_values(n: Node, a: AssemblyUnit, p1: Part, p2: Part, p3: Part) -> None:
    with sessionmanager.session() as session:
        session.add(n)
        session.add(a)
        session.add(p1)
        session.add(p2)
        session.add(p3)
        session.flush()