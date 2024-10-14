# Instrucciones para Configurar y Ejecutar el Sistema Completo (Backend, Frontend y Base de Datos)

## 1. Prerrequisitos

Asegúrate de tener las siguientes herramientas instaladas:

- **Python** (versión 3.9 o superior)
- **Node.js** (versión LTS o superior)
- **PostgreSQL**
- **Git**
- **Postman** (para pruebas de API)

---

## 2. Clonar el proyecto

En la terminal, navega a la carpeta donde quieras clonar el proyecto y ejecuta:

```bash
git clone <URL_DEL_REPOSITORIO>
cd KineCap  # Entra al directorio del proyecto
```

---

## 3. Configuración del Backend

### Paso 1: Crear entorno virtual y activar

Desde la carpeta `backend`:

```bash
cd backend
python3 -m venv venv  # Crear entorno virtual
source venv/bin/activate  # Activar entorno virtual en macOS/Linux
# En Windows: venv\Scripts\activate
```

### Paso 2: Instalar dependencias del backend

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

Si no tienes un archivo `requirements.txt`, ejecuta:

```bash
pip install Flask Flask-Cors Flask-JWT-Extended Flask-SQLAlchemy psycopg2-binary
```

### Paso 3: Configuración de la Base de Datos PostgreSQL

Accede a la consola de PostgreSQL:

```bash
psql postgres
```

Ejecuta los siguientes comandos:

```sql
CREATE USER Admin_KineCap WITH PASSWORD '1234';
CREATE DATABASE KineCap_DB;
GRANT ALL PRIVILEGES ON DATABASE KineCap_DB TO Admin_KineCap;
\q  # Salir de la consola de PostgreSQL
```

### Paso 4: Configurar la conexión con PostgreSQL en el Backend

Abre `config.py` en la carpeta `backend` y asegúrate de que la configuración sea:

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://Admin_KineCap:1234@localhost:5432/KineCap_DB'
```

### Paso 5: Crear las tablas en la base de datos

Inicia Flask en modo shell:

```bash
flask shell
```

Dentro del shell:

```python
from backend import db
db.create_all()
exit()
```

### Paso 6: Ejecutar el backend

Desde la carpeta `backend`:

```bash
flask run
```

El backend estará disponible en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 4. Configuración del Frontend

### Paso 1: Instalar dependencias del frontend

Desde la carpeta `frontend`:

```bash
cd ../frontend
npm install
```

### Paso 2: Configurar rutas en React

Asegúrate de que las rutas están configuradas correctamente en `index.js`:

```jsx
<Router>
  <Routes>
    <Route path="/" element={<Login />} />
    <Route path="/register" element={<Register />} />
    <Route path="/dashboard" element={<Dashboard />} />
  </Routes>
</Router>
```

### Paso 3: Ejecutar el frontend

Desde la carpeta `frontend`:

```bash
npm start
```

El frontend estará disponible en: [http://localhost:3000](http://localhost:3000)

---

## 5. Pruebas del Sistema usando Postman

### **Login**

1. **Método**: `POST`  
2. **URL**: `http://127.0.0.1:5000/login`  
3. **Body**:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### **Registro**

1. **Método**: `POST`  
2. **URL**: `http://127.0.0.1:5000/register`  
3. **Body**:

```json
{
  "nombre": "John",
  "apellidos": "Doe",
  "telefono": "123456789",
  "email": "john.doe@example.com",
  "pais": "Chile",
  "password": "password123"
}
```

---

## 6. Resumen de Comandos por Directorio

### **Backend** (`/KineCap/backend`)
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # (macOS/Linux)
# En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar Flask
flask run
```

### **Frontend** (`/KineCap/frontend`)
```bash
# Instalar dependencias
npm install

# Iniciar el frontend
npm start
```

### **Base de Datos PostgreSQL**
```bash
psql postgres

# Dentro de psql:
CREATE USER Admin_KineCap WITH PASSWORD '1234';
CREATE DATABASE KineCap_DB;
GRANT ALL PRIVILEGES ON DATABASE KineCap_DB TO Admin_KineCap;
\q  # Salir de psql
```

---

## 7. Verificación del Sistema

1. **Backend**:  
   - Asegúrate de que Flask está corriendo en [http://127.0.0.1:5000](http://127.0.0.1:5000).  
   - Prueba los endpoints de login y registro con Postman.

2. **Frontend**:  
   - Asegúrate de que React está corriendo en [http://localhost:3000](http://localhost:3000).  
   - Verifica que puedas navegar entre las rutas de login, registro y dashboard.

---

## 8. Solución de Problemas Comunes

1. **Error de conexión con la base de datos**:
   - Asegúrate de que PostgreSQL está corriendo.
   - Verifica las credenciales y la URI de la base de datos en `config.py`.

2. **Problemas con dependencias**:
   - Asegúrate de instalar las dependencias correctas tanto en el backend como en el frontend.

3. **CORS o problemas de política de seguridad**:
   - Verifica que `Flask-CORS` esté instalado y configurado correctamente en el backend.

---

Con estas instrucciones, podrás configurar y ejecutar el sistema completo en cualquier equipo. Si necesitas más ayuda, no dudes en pedírmelo.