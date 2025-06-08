# Proyecto Transmedina

Aplicativo web para la gestión de la empresa de transporte "TRANSMEDINA". Permite administrar conductores, mototaxis, novedades y otros recursos relacionados con la operación de la empresa.

## Tecnologías utilizadas
- **Django** (backend y lógica de negocio)
- **Bootstrap** (frontend y estilos)
- **PostgreSQL** (base de datos principal)
- **Whitenoise** (servir archivos estáticos en producción)
- **dj-database-url** y **python-dotenv** (gestión de configuración y variables de entorno)

## Instalación y ejecución local

1. **Clona el repositorio:**
   ```bash
   git clone <URL-del-repositorio>
   cd Transmedina_Project
   ```

2. **Crea y activa un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crea el archivo `.env` en la raíz del proyecto:**
   Ejemplo de contenido:
   ```env
   DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db
   LOCAL_DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
   DEBUG=True
   SECRET_KEY=tu-clave-secreta
   ```
   - `DATABASE_URL`: URL de la base de datos para producción.
   - `LOCAL_DATABASE_URL`: URL de la base de datos local para desarrollo.
   - `DEBUG`: `True` para desarrollo, `False` para producción.
   - `SECRET_KEY`: Clave secreta de Django.

5. **Realiza las migraciones y ejecuta el servidor:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. **Accede a la aplicación:**
   - Abre tu navegador en [http://localhost:8000](http://localhost:8000)

## Despliegue
- El proyecto está preparado para producción usando el archivo `Procfile` y variables de entorno.
- Configura las variables de entorno en producción según el ejemplo de `.env`.
