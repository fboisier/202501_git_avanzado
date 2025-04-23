# 🌳 Sistema de Visitas a Parques 🏞️

Una aplicación web desarrollada en Flask que permite a los usuarios registrar y compartir sus visitas a parques, así como ver y dar "Me gusta" a las visitas de otros usuarios.


## 📋 Requisitos

- 🐍 Python 3.7+
- 🐬 MySQL
- 🔮 Pipenv

## ⚙️ Configuración

<details>
<summary><b>Ver pasos de instalación</b></summary>

1. Clona este repositorio
    ```bash
    git clone https://github.com/usuario/DemoExamenParques.git
    cd DemoExamenParques
    ```

2. Configura el entorno virtual con pipenv:
    ```bash
    pipenv install
    ```

3. Configura la base de datos:
   - Crea una base de datos MySQL
   - Ejecuta el script [`parques_db.sql`](parques_db.sql) para crear las tablas necesarias:
    ```bash
    mysql -u tu_usuario -p < parques_db.sql
    ```

4. Crea un archivo [`.env`](.env) en la raíz del proyecto con la siguiente estructura:
    ```
    SECRET_KEY=tu_clave_secreta_aqui
    MYSQL_HOST=localhost
    MYSQL_USER=tu_usuario
    MYSQL_PASSWORD=tu_password
    MYSQL_DB=parques_db
    MYSQL_PORT=3306
    DEBUG=True
    ```

</details>

## 🚀 Ejecución

1. Activa el entorno virtual:
    ```bash
    pipenv shell
    ```

2. Ejecuta la aplicación:
    ```bash
    python server.py
    ```

3. Abre tu navegador en `http://localhost:5000`

## ✨ Funcionalidades

| Funcionalidad | Descripción |
|---------------|-------------|
| 👤 Autenticación | Registro e inicio de sesión con validaciones |
| 📝 Gestión de visitas | Creación, edición y eliminación de visitas a parques |
| 👀 Visualización | Visualización de visitas propias y de otros usuarios |
| ⭐ Ratings | Sistema de ratings para los parques (1-5 estrellas) |
| 👍 Me gusta | Sistema de "Me gusta" para las visitas |
| 🔢 Ordenamiento | Ordenamiento de visitas según su calificación |
| 📆 Validación de fechas | Validación para evitar registrar visitas futuras |
| 🔄 Validación de duplicados | Validación para evitar registrar visitas duplicadas al mismo parque |

## 🛠️ Tecnologías utilizadas

<div align="center">
  
  ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
  ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
  ![Bootstrap](https://img.shields.io/badge/Bootstrap_5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
  ![jQuery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)
  ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
  ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
  ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
  
</div>


## 📊 Diagrama de la base de datos

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   USUARIOS  │       │    VISITAS  │       │   PARQUES   │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id          │       │ id          │       │ id          │
│ nombre      │       │ usuario_id  │───┐   │ nombre      │
│ email       │       │ parque_id   │───┼───│ ubicacion   │
│ password    │       │ fecha       │   │   │ descripcion │
└──────┬──────┘       │ rating      │   │   └─────────────┘
       │              │ comentario  │   │
       │              └─────────────┘   │
       │                                │
       └────────────────────────────────┘
```

## 📝 Licencia

Este proyecto está bajo la licencia MIT

---

<div align="center">
  <p>👨‍💻 Desarrollado con ❤️ para mostrar mis habilidades en Flask y MySQL</p>
  <p>📧 Contacto: <a href="mailto:tucorreo@ejemplo.com">tucorreo@ejemplo.com</a></p>
</div>

---

## 📜 Poema: "Explorando la Naturaleza Digital"

*Entre líneas de código y verdor natural,*  
*un sistema que conecta humano y parque celestial.*  
*Flask y MySQL, pilares de esta creación,*  
*donde usuarios comparten su admiración.*

*Visitas registradas, momentos capturados,*  
*estrellas brillantes para parques valorados.*  
*Un lugar donde la tecnología y naturaleza se enlazan,*  
*y las experiencias verdes en bytes se transforman.*

*Desde montañas altas hasta lagos serenos,*  
*cada rincón natural en datos pequeños.*  
*Un proyecto que invita a explorar y compartir,*  
*y el amor por los parques a todos transmitir.*

*En este mundo digital de conexiones virtuales,*  
*recordamos la importancia de espacios naturales.*  
*Así, entre validaciones, rutas y sesiones,*  
*la naturaleza vive en nuestras aplicaciones.*

---

<div align="center">
  <p>🌲 DemoExamenParques - Preservando la memoria de nuestras aventuras naturales 🌲</p>
</div>