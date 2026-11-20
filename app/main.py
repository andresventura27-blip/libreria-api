from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth, models, schemas
from .database import Base, engine, get_db
from .routers import editoriales, libros

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Librería Chiapas",
    description="Proyecto Final – Taller de Desarrollo III (5°A). "
    "CRUD de libros y editoriales con autenticación Bearer Token.",
    version="1.0.0",
)


@app.get("/", tags=["General"])
def raiz():
    return {"mensaje": "API Librería Chiapas funcionando", "docs": "/docs"}


@app.post("/usuarios", response_model=schemas.UsuarioOut, status_code=201, tags=["Autenticación"])
def registrar_usuario(data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(models.Usuario).filter(models.Usuario.nomuser == data.nomuser).first():
        raise HTTPException(409, "El nombre de usuario ya existe")
    user = models.Usuario(
        nomuser=data.nomuser,
        passwd=auth.hash_password(data.passwd),
        nombrecompleto=data.nombrecompleto,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/login", response_model=schemas.Token, tags=["Autenticación"])
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Recibe `username` y `password` (formulario) y devuelve un token Bearer."""
    user = db.query(models.Usuario).filter(models.Usuario.nomuser == form.username).first()
    if not user or not auth.verify_password(form.password, user.passwd):
        raise HTTPException(
            401, "Usuario o contraseña incorrectos", headers={"WWW-Authenticate": "Bearer"}
        )
    return {"access_token": auth.create_access_token(user.nomuser), "token_type": "bearer"}


app.include_router(libros.router)
app.include_router(editoriales.router)
