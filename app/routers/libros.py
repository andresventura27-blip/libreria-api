from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import get_current_user
from ..database import get_db

router = APIRouter(prefix="/libros", tags=["Libros"])


def _validar_editorial(db: Session, editorial_id: int):
    if not db.get(models.Editorial, editorial_id):
        raise HTTPException(404, "La editorial indicada no existe")


# ---- Consultas personalizadas (van ANTES de /{id} para evitar conflictos de ruta) ----

@router.get("/sinexistencia", response_model=list[schemas.LibroOut])
def ver_libros_no_existencia(db: Session = Depends(get_db)):
    return db.query(models.Libro).filter(models.Libro.existencia == 0).all()


@router.get("/editorial/{editorial_id}", response_model=list[schemas.LibroOut])
def buscar_libros_por_editorial(editorial_id: int, db: Session = Depends(get_db)):
    _validar_editorial(db, editorial_id)
    return db.query(models.Libro).filter(models.Libro.editorial_id == editorial_id).all()


@router.get("/anio/{anio}", response_model=list[schemas.LibroOut])
def buscar_libro_anio(anio: int, db: Session = Depends(get_db)):
    return db.query(models.Libro).filter(models.Libro.anio == anio).all()


# ---- CRUD ----

@router.post("", response_model=schemas.LibroOut, status_code=201,
             dependencies=[Depends(get_current_user)])
def crear_libro(data: schemas.LibroCreate, db: Session = Depends(get_db)):
    _validar_editorial(db, data.editorial_id)
    libro = models.Libro(**data.model_dump())
    db.add(libro)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Ya existe un libro con ese ISBN")
    db.refresh(libro)
    return libro


@router.get("", response_model=list[schemas.LibroOut])
def listar_libros(db: Session = Depends(get_db)):
    return db.query(models.Libro).order_by(models.Libro.id).all()


@router.get("/{id}", response_model=schemas.LibroOut)
def obtener_libro(id: int, db: Session = Depends(get_db)):
    libro = db.get(models.Libro, id)
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
    return libro


@router.put("/{id}", response_model=schemas.LibroOut,
            dependencies=[Depends(get_current_user)])
def actualizar_libro(id: int, data: schemas.LibroCreate, db: Session = Depends(get_db)):
    libro = db.get(models.Libro, id)
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
    _validar_editorial(db, data.editorial_id)
    for campo, valor in data.model_dump().items():
        setattr(libro, campo, valor)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Ya existe un libro con ese ISBN")
    db.refresh(libro)
    return libro


@router.delete("/{id}", status_code=204, dependencies=[Depends(get_current_user)])
def eliminar_libro(id: int, db: Session = Depends(get_db)):
    libro = db.get(models.Libro, id)
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
    db.delete(libro)
    db.commit()
