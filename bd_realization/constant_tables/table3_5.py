from bd_realization.database import sessionmanager
from bd_realization.models import Table3_5_1, Table3_5_2
from sqlalchemy.orm import Session
def fill_table():
    with sessionmanager.session() as session:
        fill_part1(session)
        fill_part2(session)
        session.flush()
        session.commit()

def fill_part1(session: Session):
    session.add(Table3_5_1(m=2, cable_type="1x7", i_coef=0.0018, q=0.0032, e=0.16))
    session.add(Table3_5_1(m=3, cable_type="1x7", i_coef=0.0025, q=0.004, e=0.17))
    session.add(Table3_5_1(m=4, cable_type="1x7", i_coef=0.003, q=0.005, e=0.18))
    session.add(Table3_5_1(m=4, cable_type="1x21", i_coef=0.0011, q=0.0063, e=0.19))
    session.add(Table3_5_1(m=5, cable_type="1x21", i_coef=0.0013, q=0.007, e=0.2))
    session.add(Table3_5_1(m=7, cable_type="1x21", i_coef=0.0019, q=0.008, e=0.21))
    session.add(Table3_5_1(m=10, cable_type="1x21", i_coef=0.0025, q=0.011, e=0.22))
    

def fill_part2(session: Session):
    session.add(Table3_5_2(rubber_mark="В-14", sigma_v_s=5))
    session.add(Table3_5_2(rubber_mark="В-14-2", sigma_v_s=5.666))
    session.add(Table3_5_2(rubber_mark="ИРП1078", sigma_v_s=6.333))
    session.add(Table3_5_2(rubber_mark="НО-68-1", sigma_v_s=7))

def get_by_rubber_mark(rubber_mark: str) -> Table3_5_2 | None:
    with sessionmanager.session() as session:
        return session.query(Table3_5_2).filter(Table3_5_2.rubber_mark == rubber_mark).first()

def get_by_m_and_cable_type(m: int, cable_type: str) -> Table3_5_1 | None:
    with sessionmanager.session() as session:
        return session.query(Table3_5_1).filter(Table3_5_1.m == m, Table3_5_1.cable_type == cable_type).first()