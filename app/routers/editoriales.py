from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import get_current_user
from ..database import get_db

router = APIRouter(prefix="/editoriales", tags=["Editoriales"])


@router.post("", response_model=schemas.EditorialOut, status_code=201,
             dependencies=[Depends(get_current_user)])
def crear_editorial(data: schemas.EditorialCreate, db: Session = Depends(get_db)):
    editorial = models.Editorial(**data.model_dump())
    db.add(editorial)
    db.commit()
    db.refresh(editorial)
    return editorial


@router.get("", response_model=list[schemas.EditorialOut])
def listar_editoriales(db: Session = Depends(get_db)):
    return db.query(models.Editorial).order_by(models.Editorial.id).all()


@router.get("/{id}", response_model=schemas.EditorialOut)
def obtener_editorial(id: int, db: Session = Depends(get_db)):
    editorial = db.get(models.Editorial, id)
    if not editorial:
        raise HTTPException(404, "Editorial no encontrada")
    return editorial


@router.put("/{id}", response_model=schemas.EditorialOut,
            dependencies=[Depends(get_current_user)])
def actualizar_editorial(id: int, data: schemas.EditorialCreate, db: Session = Depends(get_db)):
    editorial = db.get(models.Editorial, id)
    if not editorial:
        raise HTTPException(404, "Editorial no encontrada")
    for campo, valor in data.model_dump().items():
        setattr(editorial, campo, valor)
    db.commit()
    db.refresh(editorial)
    return editorial


@router.delete("/{id}", status_code=204, dependencies=[Depends(get_current_user)])
def eliminar_editorial(id: int, db: Session = Depends(get_db)):
    editorial = db.get(models.Editorial, id)
    if not editorial:
        raise HTTPException(404, "Editorial no encontrada")
    if editorial.libros:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "No se puede eliminar: la editorial tiene libros asociados",
        )
    db.delete(editorial)
    db.commit()
