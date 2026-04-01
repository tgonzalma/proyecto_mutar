# MUTAR — Manual de Usuario (README)

---

1) Tipo de proyecto

- Nombre del proyecto: MUTAR
- Tipo:** [Web App / App / Plataforma / MVP]  
- Propósito: Plataforma tipo buscador de eventos y red social
- Usuario objetivo: Publico y creadores de eventos culturales
- Problema que resuelve: Facilita la búsqueda de eventos culturales a través de grupos de afinidad sin métricas de ego.
- Estado actual: MPV
- Enlaces:
  - Repositorio:

---

2) Tecnologías utilizadas

- Frontend: [HTML/CSS/Bootstrap/JS]
- Backend: [Flask, Python]
- Base de datos: [MySQL]
- Autenticación / Sesiones: [Flask-Login]
- Herramientas: [Git/GitHub, Workbench, ChatGPT]

---

3) Manual de usuario

3.1 Flujo de acceso: login y registro

- Al entrar en la web, el usuario ve la **pantalla de login**.
- Si las credenciales son correctas, el usuario accede a la página principal (**Home**).
- Si las credenciales no son válidas, se muestra un **mensaje de error** y el usuario permanece en login.
- Desde login existe un botón para ir a **registro**.
- En registro, el usuario crea su cuenta con sus **datos básicos**.
- Si el registro es exitoso, el usuario **inicia sesión automáticamente** y puede acceder a las funcionalidades internas.

---

3.2 Home: centro de la experiencia

- **Home** es el centro de la experiencia:
  - Muestra los **eventos disponibles** en formato de **grilla/listado**.
  - Cada evento muestra datos básicos como: **nombre**, **creador**, **descripción**, **fecha**, **ciudad** y **tipo de evento**.
- Home incluye una **barra de búsqueda** para localizar **usuarios** y **eventos**.
- Desde Home el usuario navega a las secciones principales: **crear eventos**, **crear grupos**, **perfil**, **favoritos** y otras rutas clave.

---

3.3 Navegación principal y menú “Mi cuenta”

La navegación principal se apoya en un menú con accesos rápidos:

- **Logo** de la plataforma: vuelve a **Home**.
- **Crear grupos**
- **Crear eventos**
- **Mi perfil**
- **Mis grupos**
- **Mis eventos**
- **Mis favoritos**
- **Mis seguidores**
- **Cerrar sesión (logout)**: elimina los datos de sesión y vuelve al login.

---

3.4 Crear y gestionar eventos

- El usuario puede **crear y gestionar** sus propios eventos.
- Desde el menú o enlaces internos se accede a la pantalla **“Crear evento”**, donde se completan campos como:
  - **Nombre del evento**
  - **Descripción**
  - **Fecha**
  - **Ciudad**
  - **Ubicación**
  - **Tipo de evento**
- Al enviar el formulario:
  - El evento se **guarda** en la base de datos.
  - El usuario se redirige a la sección **“Mis eventos”**.
- En **“Mis eventos”** el usuario ve un listado de todos los eventos que ha creado

---

3.5 Eventos favoritos y descubrimiento

- Desde la grilla/listado de eventos, el usuario puede **marcar un evento como favorito** (si está logueado).
- Los favoritos se guardan en una **tabla de relación** entre usuarios y eventos.
- En la sección **“Mis favoritos”** el usuario ve un listado de todos los eventos que marcó.
- Existe lógica para **eliminar un favorito** y mantener actualizada la lista
- Esta función ayuda al usuario a **guardar y revisar** eventos relevantes.


---

3.6 Grupos y pertenencia comunitaria

- Los **grupos** son una parte central del concepto de MUTAR.
- Cualquier usuario logueado puede **crear un grupo** indicando:
  - **Nombre**
  - **Descripción**
- El **creador** del grupo queda asociado automáticamente como **miembro**.
- En **“Mis grupos”** el usuario ve todos los grupos a los que pertenece.
- Existe la opción de **abandonar** un grupo (se elimina la relación usuario–grupo).
- A futuro, los grupos pueden funcionar como **filtros comunitarios** para descubrir eventos dentro de escenas o comunidades específicas.

---

3.7 Buscar usuarios y red de seguidores

- MUTAR incluye una capa social basada en **usuarios** y **seguidores**.
- El usuario puede **buscar personas** mediante una barra de búsqueda.
- Los resultados muestran datos básicos como:
  - **Nombre**
  - **Apellido**
  - **Nickname**
  - **Eventos creados por el usuario**
- Desde los resultados se puede **seguir** a otro usuario, creando una relación de seguimiento.
- En **“Mis seguidores”** el usuario ve:
  - Quiénes **lo siguen**
  - A quiénes **sigue**
- El objetivo es construir una red de afinidades alrededor de **eventos** y **grupos**, evitando enfocarse en métricas públicas de popularidad.

---

4) Notas y próximas actualizaciones

- Mejorar la experiencia de usuario en la creación y gestión de eventos y grupos.
- Corregir bugs detectados, como los relacionados con la gestión de favoritos.
- Implementar nuevas funcionalidades, como una vista de mapa para localizar los eventos en la ciudad y un sistema de recomendación basado en grupos y afinidades.
- Desarrollar herramientas internas para organizadores, con estadísticas centradas en la utilidad y la comunidad, evitando métricas públicas de ego.






