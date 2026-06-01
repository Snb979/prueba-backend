# Vehicles API - Backend

Backend REST para gestionar usuarios, autenticacion y vehiculos. Esta construido con FastAPI, SQLAlchemy, Alembic y MySQL.

## Requisitos

- Python 3.11 o superior
- MySQL en ejecucion
- PowerShell o una terminal compatible

## Instalacion

Desde la carpeta `backend`:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Variables de entorno

Crea un archivo `.env` en la carpeta `backend` con los valores de tu entorno:

```env
APP_NAME=Vehicles API
API_PREFIX=/api
DATABASE_URL=mysql+pymysql://root:0000@localhost:3307/vehicles_db
JWT_SECRET_KEY=change-this-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
CORS_ORIGINS=http://localhost:5173
```

Notas:

- `DATABASE_URL` debe apuntar a una base de datos MySQL existente.
- `JWT_SECRET_KEY` deberia cambiarse por un valor seguro en entornos reales.
- `CORS_ORIGINS` acepta multiples origenes separados por coma.

## Base de datos y migraciones

Alembic toma la conexion desde `DATABASE_URL`.

Crear una migracion nueva:

```powershell
.\venv\Scripts\alembic.exe revision --autogenerate -m "descripcion_del_cambio"
```

Aplicar migraciones pendientes:

```powershell
.\venv\Scripts\alembic.exe upgrade head
```

Revertir una migracion:

```powershell
.\venv\Scripts\alembic.exe downgrade -1
```

La aplicacion tambien ejecuta `Base.metadata.create_all()` al iniciar, pero se recomienda mantener el esquema controlado con Alembic.

## Ejecutar el servidor

Desde `backend` y con el entorno virtual activo:

```powershell
.\venv\Scripts\uvicorn.exe src.main:app --reload
```

La API queda disponible en:

- `http://127.0.0.1:8000`
- Documentacion Swagger: `http://127.0.0.1:8000/docs`
- Documentacion ReDoc: `http://127.0.0.1:8000/redoc`

## Estructura principal

```text
backend/
  alembic/                  Migraciones de base de datos
  src/
    core/                   Configuracion, seguridad y logging
    db/                     Conexion y sesion de SQLAlchemy
    modules/
      auth/                 Registro, login y usuario autenticado
      users/                CRUD de usuarios
      vehicles/             CRUD de vehiculos
    shared/                 Respuestas, errores y dependencias comunes
  requirements.txt
  vehicles-api.postman_collection.json
```

## Endpoints principales

Todas las rutas de negocio usan el prefijo configurado en `API_PREFIX`, por defecto `/api`.

### Auth

- `POST /api/auth/register`: registra un usuario.
- `POST /api/auth/login`: inicia sesion y devuelve un token JWT.
- `GET /api/auth/me`: devuelve el usuario autenticado.

### Users

Estas rutas requieren rol `admin`.

- `GET /api/users`: lista usuarios.
- `GET /api/users/{user_id}`: obtiene un usuario.
- `POST /api/users`: crea un usuario.
- `PUT /api/users/{user_id}`: actualiza un usuario.
- `DELETE /api/users/{user_id}`: elimina un usuario.

### Vehicles

- `GET /api/vehicles`: lista vehiculos. Requiere rol `viewer` o `admin`.
- `GET /api/vehicles/{vehicle_id}`: obtiene un vehiculo. Requiere rol `viewer` o `admin`.
- `POST /api/vehicles`: crea un vehiculo. Requiere rol `admin`.
- `PUT /api/vehicles/{vehicle_id}`: actualiza un vehiculo. Requiere rol `admin`.
- `DELETE /api/vehicles/{vehicle_id}`: elimina un vehiculo. Requiere rol `admin`.

## Autenticacion

Despues de iniciar sesion con `POST /api/auth/login`, usa el token recibido en el header:

```http
Authorization: Bearer <access_token>
```

Roles disponibles:

- `viewer`: puede consultar vehiculos.
- `admin`: puede administrar usuarios y vehiculos.

## Formato de respuesta

Las respuestas exitosas usan un envelope comun:

```json
{
  "success": true,
  "status": 200,
  "message": "Operation message",
  "data": {},
  "meta": {}
}
```

## Postman

El archivo `vehicles-api.postman_collection.json` contiene una coleccion lista para importar en Postman y probar los endpoints.
