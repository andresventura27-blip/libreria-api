# API REST – Librería Chiapas

Proyecto Final de Taller de Desarrollo III (5.º A) – LIDTS, ETDA CIV, UNACH.
API REST para administrar libros y editoriales, con autenticación Bearer Token.

**URL de producción:** https://REEMPLAZAR.onrender.com
**Documentación interactiva:** https://REEMPLAZAR.onrender.com/docs

## Tecnologías
Python 3.12 · FastAPI · Uvicorn · Pydantic · SQLAlchemy 2 · PostgreSQL · PyJWT (Bearer Token) · Render

## Estructura
```
libreria-api/
├── app/
│   ├── main.py          # App, /login, /usuarios
│   ├── models.py        # Editorial, Libro, Usuario
│   ├── schemas.py       # Esquemas Pydantic
│   ├── database.py      # Conexión a PostgreSQL
│   ├── auth.py          # Hash de contraseñas y tokens
│   └── routers/
│       ├── libros.py
│       └── editoriales.py
├── seed.py              # Datos de prueba
├── requirements.txt
├── render.yaml
└── README.md
```

## Instalación y ejecución local
1. Crear la base de datos en PostgreSQL:
   ```sql
   CREATE DATABASE libreria;
   ```
2. Entorno virtual e instalación:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Configuración: copiar `.env.example` a `.env` y ajustar `DATABASE_URL` y `SECRET_KEY`.
4. Cargar datos de prueba (crea las tablas y el usuario `admin` / `admin123`):
   ```bash
   python seed.py
   ```
5. Ejecutar:
   ```bash
   uvicorn app.main:app --reload
   ```
   Documentación en http://127.0.0.1:8000/docs

## Autenticación
1. `POST /usuarios` registra un usuario (`nomuser`, `passwd`, `nombrecompleto`); la contraseña se guarda con hash PBKDF2.
2. `POST /login` recibe `username` y `password` como **form-data / x-www-form-urlencoded** y devuelve:
   ```json
   { "access_token": "eyJ...", "token_type": "bearer" }
   ```
3. En los endpoints protegidos se envía `Authorization: Bearer <token>`.
   Sin token o con token inválido se responde `401 Unauthorized`.

Protegidos: `POST`, `PUT` y `DELETE` de `/libros` y `/editoriales`. Los `GET` son públicos.

## Endpoints
| Método | Ruta | Protegido |
|---|---|---|
| POST | /login | No |
| POST | /usuarios | No |
| POST / GET | /libros | POST sí |
| GET / PUT / DELETE | /libros/{id} | PUT, DELETE sí |
| GET | /libros/sinexistencia | No |
| GET | /libros/editorial/{editorial_id} | No |
| GET | /libros/anio/{anio} | No |
| POST / GET | /editoriales | POST sí |
| GET / PUT / DELETE | /editoriales/{id} | PUT, DELETE sí |

## Ejemplos
```bash
curl -X POST https://REEMPLAZAR.onrender.com/login -d "username=admin&password=admin123"

curl https://REEMPLAZAR.onrender.com/libros/anio/2020

curl -X POST https://REEMPLAZAR.onrender.com/libros \
  -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
  -d '{"titulo":"Ficciones","autor":"Jorge Luis Borges","isbn":"9788420633121","anio":1944,"existencia":5,"editorial_id":1}'
```

## Despliegue en Render
1. Subir el proyecto a GitHub.
2. En Render: **New → PostgreSQL** (plan Free). Copiar la *Internal Database URL*.
3. **New → Web Service**, conectar el repositorio:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Variables de entorno: `DATABASE_URL` (la del paso 2), `SECRET_KEY` (cadena aleatoria larga), `PYTHON_VERSION=3.12.8`
4. Cargar datos de prueba en producción: ejecutar `python seed.py` desde tu equipo con `DATABASE_URL` apuntando a la *External Database URL*, o desde la pestaña Shell del servicio.
## URL de producción
- API: https://libreria-api-1wmf.onrender.com
- Documentación: https://libreria-api-1wmf.onrender.com/docs
