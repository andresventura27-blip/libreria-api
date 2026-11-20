from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class Editorial(Base):
    __tablename__ = "editoriales"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    pais: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)

    libros: Mapped[list["Libro"]] = relationship(back_populates="editorial")


class Libro(Base):
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    autor: Mapped[str] = mapped_column(String(150), nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    anio: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    existencia: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    editorial_id: Mapped[int] = mapped_column(
        ForeignKey("editoriales.id"), nullable=False, index=True
    )

    editorial: Mapped[Editorial] = relationship(back_populates="libros")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nomuser: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    passwd: Mapped[str] = mapped_column(String(255), nullable=False)  # hash, nunca texto plano
    nombrecompleto: Mapped[str] = mapped_column(String(150), nullable=False)
