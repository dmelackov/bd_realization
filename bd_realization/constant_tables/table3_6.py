from bd_realization.database import sessionmanager
from bd_realization.models import Table3_6
def fill_table():
    with sessionmanager.session() as session:
        session.add(Table3_6(machine_type="Деревообрабатывающее оборудование", peak_load=100, K_d=1.1))
        session.add(Table3_6(machine_type="Деревообрабатывающее оборудование", peak_load=250, K_d=1.2))
        session.add(Table3_6(machine_type="Деревообрабатывающее оборудование", peak_load=400, K_d=None))
        session.add(Table3_6(machine_type="Токарные станки и оборудование для типографии", peak_load=100, K_d=1.2))
        session.add(Table3_6(machine_type="Токарные станки и оборудование для типографии", peak_load=250, K_d=1.4))
        session.add(Table3_6(machine_type="Токарные станки и оборудование для типографии", peak_load=400, K_d=1.6))
        session.add(Table3_6(machine_type="Сверлильные, расточные, шлифовальные, фрезерные, поперечно-строгальные и долбежные станки", peak_load=100, K_d=1.3))
        session.add(Table3_6(machine_type="Сверлильные, расточные, шлифовальные, фрезерные, поперечно-строгальные и долбежные станки", peak_load=250, K_d=1.5))
        session.add(Table3_6(machine_type="Сверлильные, расточные, шлифовальные, фрезерные, поперечно-строгальные и долбежные станки", peak_load=400, K_d=1.7))
        session.add(Table3_6(machine_type="Конвейеры ленточные", peak_load=100, K_d=1.4))
        session.add(Table3_6(machine_type="Конвейеры ленточные", peak_load=250, K_d=1.5))
        session.add(Table3_6(machine_type="Конвейеры ленточные", peak_load=400, K_d=1.6))
        session.add(Table3_6(machine_type="Вентиляторы, подъемники и текстильное оборудование", peak_load=100, K_d=1.4))
        session.add(Table3_6(machine_type="Вентиляторы, подъемники и текстильное оборудование", peak_load=250, K_d=1.6))
        session.add(Table3_6(machine_type="Вентиляторы, подъемники и текстильное оборудование", peak_load=400, K_d=1.8))
        session.add(Table3_6(machine_type="Пластинчатый, ковшовый и элеваторный конвейеры", peak_load=100, K_d=1.5))
        session.add(Table3_6(machine_type="Пластинчатый, ковшовый и элеваторный конвейеры", peak_load=250, K_d=1.6))
        session.add(Table3_6(machine_type="Пластинчатый, ковшовый и элеваторный конвейеры", peak_load=400, K_d=1.7))
        session.add(Table3_6(machine_type="Скребковый и шнековый конвейер", peak_load=100, K_d=1.5))
        session.add(Table3_6(machine_type="Скребковый и шнековый конвейер", peak_load=250, K_d=1.7))
        session.add(Table3_6(machine_type="Скребковый и шнековый конвейер", peak_load=400, K_d=1.8))
        session.flush()
        session.commit()

def get_by_peak_load_and_machine_type(load: int, machine_type: str) -> Table3_6 | None:
    with sessionmanager.session() as session:
        return session.query(Table3_6).filter(Table3_6.peak_load >= load, Table3_6.machine_type == machine_type).first()