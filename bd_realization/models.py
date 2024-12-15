from re import M
from unittest import result
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Table3_5_1(Base):
    __tablename__ = "table3_5_1"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    m: Mapped[int]
    cable_type: Mapped[str]
    q: Mapped[float]
    e: Mapped[float]
    i_coef: Mapped[float]


class Table3_5_2(Base):
    __tablename__ = "table3_5_2"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    rubber_mark: Mapped[str]
    sigma_v_s: Mapped[float]

class Table3_6(Base):
    __tablename__ = "table3_6"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    machine_type: Mapped[str]
    peak_load: Mapped[int]
    K_d: Mapped[float | None] = mapped_column(nullable=True)


class Node(Base):
    __tablename__ = "node"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    assembly_units: Mapped[list["AssemblyUnit"]] = relationship()

    machine_mode: Mapped[str | None] = mapped_column(nullable=True)
    shift_mode: Mapped[str | None] = mapped_column(nullable=True)


class AssemblyUnit(Base):
    __tablename__ = "assembly_unit"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    node_id: Mapped[int] = mapped_column(ForeignKey("node.id"))
    node: Mapped[Node] = relationship(back_populates="assembly_units")
    parts: Mapped[list["Part"]] = relationship()

    NSE: Mapped[str]
    TSE: Mapped[str]
    VSE: Mapped[str]

    i: Mapped[int | None] = mapped_column(nullable=True)
    result: Mapped[str | None] = mapped_column(nullable=True)
    K_d: Mapped[float | None] = mapped_column(nullable=True)
    K: Mapped[float | None] = mapped_column(nullable=True)
    K_p: Mapped[float | None] = mapped_column(nullable=True)
    phi: Mapped[float | None] = mapped_column(nullable=True)
    N_c: Mapped[float | None] = mapped_column(nullable=True)
    phi_t: Mapped[float | None] = mapped_column(nullable=True)
    phi_c: Mapped[float | None] = mapped_column(nullable=True)
    phi_p: Mapped[float | None] = mapped_column(nullable=True)
    i_coef: Mapped[float | None] = mapped_column(nullable=True)
    j: Mapped[float | None] = mapped_column(nullable=True)
    status1: Mapped[str | None] = mapped_column(nullable=True)
    status2: Mapped[str | None] = mapped_column(nullable=True)
    working_mode: Mapped[str | None] = mapped_column(nullable=True)
    roller_count: Mapped[int | None] = mapped_column(nullable=True)
    beta: Mapped[float | None] = mapped_column(nullable=True)
    delta_t_k: Mapped[float | None] = mapped_column(nullable=True)
    a: Mapped[float | None] = mapped_column(nullable=True)
    t_ch: Mapped[float | None] = mapped_column(nullable=True)
    t_ch_j: Mapped[float | None] = mapped_column(nullable=True)
    F: Mapped[float | None] = mapped_column(nullable=True)
    peak_load: Mapped[float | None] = mapped_column(nullable=True)
    F1: Mapped[float | None] = mapped_column(nullable=True)
    F_j: Mapped[float | None] = mapped_column(nullable=True)
    F_pred: Mapped[float | None] = mapped_column(nullable=True)


class Part(Base):
    __tablename__ = "part"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    assembly_unit_id: Mapped[int] = mapped_column(ForeignKey("assembly_unit.id"))
    assembly_unit: Mapped[AssemblyUnit] = relationship(back_populates="parts")

    ND: Mapped[str]
    NAD: Mapped[str | None] = mapped_column(nullable=True)

    z0: Mapped[float | None] = mapped_column(nullable=True)
    z1: Mapped[float | None] = mapped_column(nullable=True)
    z2: Mapped[float | None] = mapped_column(nullable=True)
    z_p: Mapped[float | None] = mapped_column(nullable=True)
    rubber_mark: Mapped[str | None] = mapped_column(nullable=True)
    e: Mapped[float | None] = mapped_column(nullable=True)
    cable_type: Mapped[str | None] = mapped_column(nullable=True)
    S1: Mapped[float | None] = mapped_column(nullable=True)
    b: Mapped[float | None] = mapped_column(nullable=True)
    gamma: Mapped[float | None] = mapped_column(nullable=True)
    d_a1: Mapped[float | None] = mapped_column(nullable=True)
    m: Mapped[float | None] = mapped_column(nullable=True)
    h: Mapped[float | None] = mapped_column(nullable=True)
    alpha1: Mapped[float | None] = mapped_column(nullable=True)
    S: Mapped[float | None] = mapped_column(nullable=True)
    n1: Mapped[float | None] = mapped_column(nullable=True)
    n_j: Mapped[float | None] = mapped_column(nullable=True)
    v: Mapped[float | None] = mapped_column(nullable=True)
    sigma_sd: Mapped[float | None] = mapped_column(nullable=True)
    sigma_sd_dop: Mapped[float | None] = mapped_column(nullable=True)
    Q0: Mapped[float | None] = mapped_column(nullable=True)
    F_c: Mapped[float | None] = mapped_column(nullable=True)
    sigma_sd_diff: Mapped[float | None] = mapped_column(nullable=True)
    F_diff: Mapped[float | None] = mapped_column(nullable=True)
    sigma_sd_: Mapped[float | None] = mapped_column(nullable=True)