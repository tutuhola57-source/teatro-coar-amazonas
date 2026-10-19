# 🎭 MANUAL OPERATIVO PARA LA GESTIÓN DE ARCHIVOS, LIBRETOS Y PUESTAS EN ESCENA
## Plataforma Web del Elenco de Teatro — COAR Amazonas

> **Documento de consulta pedagógica y técnica para el profesor asesor**  
> *Colegio de Alto Rendimiento Amazonas — Chachapoyas, Perú*  
> *Versión 1.0 — Guía de autogestión sin necesidad de programas complejos ni terminales de comandos*

---

## 1. Introducción y Propósito

Estimado colega asesor:

Esta plataforma web no es un escaparate estático ni una tarea informática decorativa: **es el cofre de la memoria viva del Elenco de Teatro del COAR Amazonas**. 

En la dinámica particular de nuestro colegio con régimen de internado en Chachapoyas, las promociones de estudiantes transitan año tras año. Los estudiantes de 5.° de secundaria que hoy dominan la proyección de la voz, el diseño de luces y la caracterización de personajes se graduarán muy pronto. Para que ese conocimiento artístico acumulado no se desvanezca en carpetas olvidadas o memorias USB extraviadas, esta plataforma garantiza que:

1. **Los libretos adaptados y corregidos en mesa de lectura permanezcan accesibles** para que las promociones de 3.° y 4.° de secundaria puedan reponer las obras o estudiar sus estructuras dramáticas.
2. **Las fichas de caracterización y reparto reconozcan el esfuerzo y la sensibilidad** de los estudiantes que dieron vida a cada papel en el Salón de Usos Múltiples (SUM) o en el patio central.
3. **Las bitácoras técnicas (sonido, iluminación, utilería)** sirvan de guía para que los futuros montajes no empiecen de cero.
4. **Cualquier estudiante o docente pueda consultar e imprimir el texto dramático** en cualquier momento, desde cualquier computadora del colegio o desde su celular.

Esta guía está diseñada paso a paso para que puedas gestionar todo el material directamente desde tu navegador de internet favorito (Google Chrome, Microsoft Edge, Mozilla Firefox), sin instalar software complejo, sin comandos y con total tranquilidad.

---

## 2. Cómo Descargar y Respaldar Archivos

Mantener copias de seguridad es fundamental frente a caídas temporales de internet o para trabajar durante los ensayos en espacios sin conexión.

### A. Descarga directa desde la web pública (para estudiantes y ensayos)
Cualquier integrante del elenco puede descargar los libretos de manera inmediata:

1. Ingresa a la página oficial del taller:  
   👉 **[https://tutuhola57-source.github.io/teatro-coar-amazonas/](https://tutuhola57-source.github.io/teatro-coar-amazonas/)**
2. Desplázate hacia abajo hasta la sección **"Banco de Libretos y Guiones en PDF"** (o haz clic en el menú superior en *Libretos*).
3. Cada obra tiene una tarjeta con su título, autor, grado y número de personajes.
4. Haz clic en el botón oscuro con borde dorado: **"Descargar Libreto"**.
5. El archivo PDF se descargará automáticamente en tu dispositivo, listo para ser impreso para la lectura en mesa o enviado al grupo de estudio del elenco.

> [!TIP]
> Si los estudiantes necesitan ensayar en las aulas o en los jardines del internado donde la señal WiFi no llega con fuerza, sugiéreles descargar el PDF en sus tabletas o imprimir un juego de libretos con anticipación.

---

### B. Descarga de respaldo maestro completo (Copia de seguridad en USB o Laptop)
Como asesor, es una buena práctica docente realizar una copia de seguridad general de todo el proyecto (textos, código, fichas e imágenes) al término de cada trimestre o tras el estreno de una obra.

1. Abre tu navegador e ingresa al repositorio central en GitHub:  
   👉 **[https://github.com/tutuhola57-source/teatro-coar-amazonas](https://github.com/tutuhola57-source/teatro-coar-amazonas)**
2. En la parte superior derecha de la lista de archivos, busca el **botón verde que dice `< > Code`**.
3. Al hacer clic, se desplegará un menú emergente.
4. Haz clic en la última opción: **`Download ZIP`**.
5. Se descargará un archivo comprimido llamado `teatro-coar-amazonas-main.zip` que contiene **absolutamente todos los archivos del taller**.
6. Guarda este archivo en tu memoria USB personal o en la carpeta de respaldos de tu laptop de trabajo.

```
+-----------------------------------------------------------+
| Repositorio: teatro-coar-amazonas                         |
| [ <> Code ▼ ]  <--- Clic aquí                             |
|   |-- Clone / Open with GitHub Desktop                    |
|   |-- Download ZIP  <--- Clic para descargar respaldo    |
+-----------------------------------------------------------+
```

---

## 3. Cómo Subir Nuevos Libretos en PDF (Vía Web, Sin Instalar Nada)

Cuando termines de adaptar una nueva obra o de digitalizar un guion en formato PDF, puedes subirlo directamente a la plataforma usando la interfaz web de GitHub.

### Paso 1: Ingresar a la carpeta de libretos
1. Entra a **[https://github.com/tutuhola57-source/teatro-coar-amazonas](https://github.com/tutuhola57-source/teatro-coar-amazonas)**.
2. En la lista de carpetas, haz clic sobre la carpeta **`public`**.
3. Dentro de `public`, haz clic sobre la subcarpeta **`libretos`**.  
   *(La ruta que verás en pantalla será `teatro-coar-amazonas / public / libretos`)*.

### Paso 2: Activar la subida de archivos
1. En la esquina superior derecha de la lista de archivos, verás un botón que dice **`Add file`** (con una pequeña flecha hacia abajo).
2. Haz clic en **`Add file`** y selecciona la opción **`Upload files`**.

### Paso 3: Arrastrar el documento PDF
1. Se abrirá una ventana con una caja de líneas punteadas que dice:  
   *“Drag files here to add them to your repository or choose your files”*.
2. Abre la carpeta de tu computadora donde tienes guardado el libreto en PDF y **arrástralo hacia la caja con el ratón** (o haz clic en *choose your files* para buscarlo en tu disco).
3. Verás una barra de progreso que indica que el archivo se ha cargado.

> [!IMPORTANT]
> **Regla de oro para el nombre del archivo PDF:**
> Para evitar errores en internet, el nombre del archivo debe estar en **minúsculas, sin espacios, sin tildes, sin eñes ni caracteres especiales**, usando guiones normales `-`.  
> - ✅ **Correcto:** `ollantay-adaptacion-2026.pdf`  
> - ❌ **Incorrecto:** `Libreto Ollantay (Final) 4to año.pdf`  
> 
> *Anota mentalmente ese nombre (por ejemplo `ollantay-adaptacion-2026`), porque lo necesitarás en el paso siguiente.*

### Paso 4: Confirmar el guardado (Commit)
1. Desplázate hacia el final de la página web. Verás una sección titulada **`Commit changes`**.
2. En el primer campo de texto (*Commit message*), escribe una frase sencilla y humana que describa lo que hiciste, por ejemplo:  
   `Subir libreto en PDF de Ollantay 2026`
3. Asegúrate de que esté seleccionada la opción por defecto:  
   🔘 *Commit directly to the `main` branch*.
4. Haz clic en el botón verde **`Commit changes`** (o *Propose changes*).
5. ¡Listo! El archivo PDF ya está guardado en el servidor del taller.

---

## 4. Cómo Vincular la Nueva Obra en el Catálogo Web (Editar `src/data/obras.json`)

Una vez subido el PDF, el siguiente paso es registrar los datos de la obra (el título, el autor, el grado, la sinopsis, el reparto de actores y la ficha técnica) para que aparezca automáticamente en la cartelera principal y en el banco de libretos.

Todos los datos se guardan en un único archivo de texto llamado **`obras.json`**, ubicado dentro de la carpeta `src/data/`.

### Paso 1: Abrir el archivo de datos en GitHub
1. Regresa a la portada del repositorio: **[https://github.com/tutuhola57-source/teatro-coar-amazonas](https://github.com/tutuhola57-source/teatro-coar-amazonas)**.
2. Haz clic en la carpeta **`src`**.
3. Haz clic en la carpeta **`data`**.
4. Haz clic sobre el archivo **`obras.json`**.

### Paso 2: Entrar en el modo de edición
1. En la barra superior del archivo (hacia la derecha), verás el **ícono de un pequeño lápiz** ✏️ (*Edit this file*).
2. Haz clic en el lápiz. El archivo se convertirá en un editor de texto interactivo dentro de tu navegador.

### Paso 3: Pegar la nueva obra dentro de la lista
1. Localiza el bloque `"obras": [` (que comienza cerca de la línea 13).
2. Cada obra está contenida entre llaves `{ ... }` y separada de la siguiente por una coma `,`.
3. Puedes insertar tu nueva obra al inicio de la lista (para que aparezca primero en la web) o al final.

#### 📋 Plantilla modelo lista para copiar, pegar y completar:

Copia este bloque modelo, pégalo dentro de `"obras": [` y cambia los textos con la información real de tu montaje:

```json
    {
      "id": "ollantay-adaptacion-2026",
      "titulo": "Ollantay (Adaptación Escolar)",
      "autor": "Dramaturgia Andina Colonial • Versión COAR Amazonas",
      "anio": "2026",
      "grado": "4.° de Secundaria",
      "genero": "Drama Histórico Épico",
      "duracion": "45 min",
      "sinopsis": "En el corazón del Tahuantinsuyo, el valeroso general Ollantay desafía los mandatos de casta del Inca Pachacútec al declarar su amor por la princesa Cusi Coyllur. Montaje adaptado con coro escénico y sonorización en vivo por los estudiantes del internado.",
      "portada": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?auto=format&fit=crop&w=1000&q=80",
      "fotos_escena": [
        "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1469488865564-c2de10f69f96?auto=format&fit=crop&w=1000&q=80"
      ],
      "pdf_libreto": "libretos/ollantay-adaptacion-2026.pdf",
      "pdf_tamano": "Libreto PDF (1.8 MB)",
      "reparto": [
        { "personaje": "Ollantay", "actor": "Estudiante de 4.° A — General del Antisuyo" },
        { "personaje": "Cusi Coyllur", "actor": "Estudiante de 4.° B — Hija del Inca Pachacútec" },
        { "personaje": "Inca Pachacútec", "actor": "Estudiante de 4.° C — Máxima autoridad imperial" },
        { "personaje": "Piqui Chaqui", "actor": "Estudiante de 4.° A — Siervo leal y contraparte cómica" },
        { "personaje": "Rumiñahui", "actor": "Estudiante de 4.° B — General del Hanan Cusco" },
        { "personaje": "Ima Súmac", "actor": "Estudiante de 4.° C — Joven hija del amor prohibido" }
      ],
      "ficha_tecnica": {
        "direccion": "Profesor Asesor del Taller de Teatro",
        "luces": "Luz cenital cálida para monólogos, penumbra azul para la prisión y antorchas simuladas",
        "sonido": "Quenas, charango, tambor andino y efectos de viento de ceja de selva grabados en patio"
      }
    },
```

> [!WARNING]
> **Consejos vitales para no romper el formato:**
> 1. **La correspondencia del `id`:** El campo `"id"` (ejemplo: `"ollantay-adaptacion-2026"`) **debe coincidir exactamente con el nombre de tu archivo PDF** que subiste a `public/libretos/` (es decir, `ollantay-adaptacion-2026.pdf`). La plataforma web usa este identificador para vincular el botón de descarga directa.
> 2. **Las comas `,`:** Cada línea dentro de un bloque lleva una coma al final, **excepto la última línea** antes de cerrar la llave `}` o el corchete `]`.
> 3. **Las comillas dobles `"`:** Todos los textos y nombres de campos deben estar encerrados en comillas dobles rectas `"texto"`. No uses comillas tipográficas curvadas ni dejes comillas sin cerrar.

### Paso 4: Guardar los cambios
1. Una vez pegado y revisado el texto, baja hasta el final de la página.
2. En la caja de **`Commit changes`**, escribe:  
   `Agregar obra Ollantay al catálogo 2026`
3. Haz clic en el botón verde **`Commit changes`**.

---

## 5. Cómo Subir o Reemplazar Fotografías de Ensayos y Estrenos

El registro visual preserva la emoción de las funciones en el colegio. Tienes dos caminos muy sencillos para gestionar las fotos:

### Opción A: Subir las fotos directamente al repositorio (Recomendado para fotos oficiales)
1. Navega en GitHub a la carpeta **`public`**.
2. Haz clic en **`Add file`** -> **`Upload files`**.
3. Arrastra tu fotografía (asegúrate de que esté en formato JPG o PNG y con un nombre simple, como `foto-estreno-ollantay-1.jpg`).
4. Haz clic en **`Commit changes`**.
5. Ahora, en el archivo `src/data/obras.json`, vincula la foto usando su ruta relativa o el nombre del archivo:
   ```json
   "portada": "foto-estreno-ollantay-1.jpg",
   ```

### Opción B: Usar enlaces directos de alta resolución (Ideal para galerías fotográficas amplias)
Si el taller cuenta con cientos de fotos del estreno tomadas por el equipo de prensa escolar o subidas a la nube del colegio:
1. Sube las fotografías a un servidor de imágenes o álbum público escolar (como Google Drive con enlace público directo, Imgur o Unsplash si son imágenes conceptuales de referencia).
2. Copia la URL directa de la imagen (debe terminar en `.jpg`, `.jpeg` o `.png`).
3. Pégala en el campo `"portada"` o agrégala a la lista de `"fotos_escena"`:
   ```json
   "fotos_escena": [
     "https://miservidor.edu.pe/fotos/teatro/ensayo-noche-1.jpg",
     "https://miservidor.edu.pe/fotos/teatro/estreno-elenco-2026.jpg"
   ]
   ```

> [!TIP]
> **Recomendación para las fotos:**  
> - Usa fotos en orientación **horizontal** (apaisadas) para que se vean perfectas en las tarjetas y en la ventana emergente de detalles.  
> - Procura que no pesen más de **2 MB** cada una para que la página cargue con rapidez, incluso en las computadoras más lentas de la biblioteca escolar.

---

## 6. Cómo se Publica Automáticamente (La Magia de GitHub Actions)

Una de las mayores ventajas de esta plataforma es que **tú no necesitas compilar nada, ni pagar hosting, ni llamar a un programador cada vez que hagas un cambio**.

### ¿Qué ocurre cuando haces clic en "Commit changes"?
1. Tan pronto como guardas un cambio en `obras.json` o subes un nuevo PDF a `public/libretos/`, se activa en los servidores de GitHub un asistente automático llamado **GitHub Actions**.
2. Este asistente invisible:
   - Lee los nuevos libretos e imágenes.
   - Reconstruye la página web completa con Astro.
   - Actualiza de forma segura la versión pública en GitHub Pages.
3. Todo este proceso ocurre en la nube y **tarda entre 60 y 120 segundos**.

### ¿Cómo verificar que la web se actualizó con éxito?
1. En la parte superior del repositorio en GitHub, haz clic en la pestaña que dice **`Actions`** (ubicada entre *Pull requests* y *Projects*).
2. Verás una lista de ejecuciones con un círculo:
   - 🟡 **Círculo amarillo girando:** El sistema está procesando y construyendo la nueva versión. Solo debes esperar un minuto.
   - 🟢 **Círculo verde con check (✔):** La página web ya se actualizó correctamente y está visible en internet con tus nuevos libretos.
   - 🔴 **Círculo rojo con cruz (✖):** Hubo un error de sintaxis en el archivo que editaste (generalmente una coma faltante o una comilla en `obras.json`). Consulta la siguiente sección para solucionarlo en dos minutos.

```
Pestaña Actions en GitHub:
  [✔] Deploy to GitHub Pages ............ Hace 1 minuto  (¡Publicación exitosa!)
```

---

## 7. Preguntas Frecuentes y Soporte Pedagógico

### ❓ ¿Qué pasa si me equivoqué en una coma o comilla y la pestaña Actions se puso roja ❌?
¡No te alarmes! En GitHub **nada se destruye ni se pierde**. Si el sistema se puso en rojo, significa que encontró un error de puntuación en `obras.json` y, para proteger la web, no publicó el cambio roto.
- **Solución:**
  1. Vuelve a entrar a `src/data/obras.json` y haz clic en el lápiz ✏️.
  2. Revisa el último bloque que pegaste. Busca:
     - ¿Falta una comilla de cierre? (ejemplo: `"titulo": "Ollantay`).
     - ¿Pusiste una coma al final del último elemento antes de cerrar la llave? (borra esa coma sobrante).
     - ¿Olvidaste la coma que separa tu nueva obra de la obra anterior? (agrégala).
  3. Haz clic nuevamente en **`Commit changes`**. El asistente volverá a intentar la publicación de inmediato.

---

### ❓ ¿Hay un límite de peso para los archivos PDF de los libretos?
- Los libretos de texto puro suelen pesar menos de **1 o 2 MB**. En esos casos, suben de forma instantánea.
- Si tu libreto incluye fotografías a color, partituras escaneadas o portadas muy pesadas, procura que el archivo **no supere los 20 o 25 MB**.
- **Consejo práctico:** Si tu PDF pesa 40 o 50 MB, puedes usar una herramienta gratuita en línea como *ilovepdf.com* o *smallpdf.com* en la opción "Comprimir PDF" antes de subirlo. Esto asegurará que los estudiantes puedan descargarlo rápidamente desde sus celulares sin agotar sus datos móviles.

---

### ❓ ¿Cómo respaldar en Google Drive institucional?
Si el colegio utiliza Google Workspace para Educación:
1. Crea una carpeta en tu Google Drive llamada:  
   📁 `COAR Amazonas - Archivo Teatral y Libretos`.
2. Dentro de esa carpeta, crea dos subcarpetas:  
   - `01_Libretos_Originales_Word_y_PDF` (para guardar tus archivos editables en Word antes de convertirlos a PDF).  
   - `02_Respaldos_Plataforma_Web` (para subir el archivo `.zip` que descargas desde GitHub al final de cada ciclo).  
   - `03_Fotos_Sin_Comprimir` (para las fotos tomadas con cámara réflex durante las funciones).
3. Comparte esa carpeta con la Dirección Académica o con el docente de Arte del colegio para garantizar la continuidad pedagógica institucional si algún día cambias de sede.

---

### ❓ ¿Cómo editar una ficha de personaje ya existente?
Si un estudiante cambia de personaje o deseas afinar la descripción psicológica de un rol:
1. Abre `src/data/obras.json` en GitHub con el ícono del lápiz ✏️.
2. Busca la obra correspondiente.
3. Dentro de `"reparto": [ ... ]`, localiza la línea del personaje y edita directamente el texto entre comillas:
   ```json
   { "personaje": "Mateo", "actor": "El Brigadier — Nueva descripción del rol aquí" }
   ```
4. Guarda los cambios con **`Commit changes`** y en un par de minutos estará reflejado en la web.

---

## 8. Resumen Rápido de Rutas y Enlaces Clave

| Elemento | Enlace o Ruta en el Repositorio | Propósito |
| :--- | :--- | :--- |
| **Sitio Web Público** | `https://tutuhola57-source.github.io/teatro-coar-amazonas/` | Portal visible para estudiantes, familias y público general. |
| **Repositorio Central** | `https://github.com/tutuhola57-source/teatro-coar-amazonas` | Panel de control web para gestionar los archivos. |
| **Carpeta de Libretos** | `public/libretos/` | Lugar donde se suben los nuevos documentos en PDF. |
| **Catálogo de Obras** | `src/data/obras.json` | Archivo de datos donde se registran sinopsis, personajes y fichas. |
| **Estado de Publicación** | Pestaña `Actions` en GitHub | Indicador en tiempo real de la actualización del sitio web. |

---

*“El teatro en la escuela no es solo el texto que se dice en el escenario, sino el puente humano que une a una generación con la que viene después.”*  
**Elenco de Teatro & Creación Escénica — COAR Amazonas**
