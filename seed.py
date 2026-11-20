"""Carga datos de prueba: python seed.py"""
from app import auth, models
from app.database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if not db.query(models.Usuario).first():
    db.add(models.Usuario(nomuser="admin", passwd=auth.hash_password("admin123"),
                          nombrecompleto="Administrador"))

if not db.query(models.Editorial).first():
    eds = [
        models.Editorial(nombre="Penguin Random House", pais="Estados Unidos", email="contacto@prh.com"),
        models.Editorial(nombre="Fondo de Cultura Económica", pais="México", email="info@fce.com.mx"),
        models.Editorial(nombre="Planeta", pais="España", email="info@planeta.es"),
    ]
    db.add_all(eds)
    db.flush()
    db.add_all([
        models.Libro(titulo="Cien años de soledad", autor="Gabriel García Márquez", isbn="9780307474728", anio=1967, existencia=0, editorial_id=eds[0].id),
        models.Libro(titulo="Pedro Páramo", autor="Juan Rulfo", isbn="9786071600196", anio=1955, existencia=12, editorial_id=eds[1].id),
        models.Libro(titulo="El laberinto de la soledad", autor="Octavio Paz", isbn="9786071601209", anio=1950, existencia=0, editorial_id=eds[1].id),
        models.Libro(titulo="La sombra del viento", autor="Carlos Ruiz Zafón", isbn="9788408172178", anio=2001, existencia=7, editorial_id=eds[2].id),
        models.Libro(titulo="Los detectives salvajes", autor="Roberto Bolaño", isbn="9788433974983", anio=1998, existencia=4, editorial_id=eds[2].id),
        models.Libro(titulo="Hábitos atómicos", autor="James Clear", isbn="9786077475705", anio=2020, existencia=15, editorial_id=eds[0].id),
        models.Libro(titulo="El infinito en un junco", autor="Irene Vallejo", isbn="9788418436000", anio=2020, existencia=3, editorial_id=eds[2].id),
    ])

db.commit()
db.close()
print("Datos de prueba cargados. Usuario: admin / admin123")
