# 🏛️ GUÍA MAESTRA DE TRASPASO INSTITUCIONAL Y AUTONOMÍA TOTAL
## Taller de Teatro & Creación Escénica — COAR Amazonas
### Sistema de Publicación Desatendida en la Nube y Gestión de Bajas sin Emerson

> **Documento de transferencia tecnológica e institucional**  
> *Diseñado para que el profesor asesor y las futuras generaciones de estudiantes gestionen la plataforma de forma 100% autónoma, sin depender de la laptop de Emerson ni requerir conocimientos de programación.*

---

## 1. El Gran Desafío: ¿Qué pasa cuando Emerson se gradúa?

Una plataforma escolar exitosa es aquella que **sobrevive a sus fundadores**. Para que el archivo de libretos no se detenga cuando Emerson culmine su etapa en el COAR Amazonas, la arquitectura ha sido configurada bajo tres principios:

1. **Cero Dependencia de Hardware Local:** El profesor asesor no necesita la computadora de Emerson encendida ni una terminal de comandos.
2. **Entorno Familiar (Google Drive):** El profesor y los comités estudiantiles gestionan los libretos desde el Google Drive que ya usan todos los días en el colegio.
3. **Control Total de Publicaciones y Bajas:** Se puede tanto **publicar** nuevas obras como **dar de baja / retirar** montajes erróneos en segundos.

---

## 2. Cómo Funciona el Buzón Inteligente en Google Drive

La carpeta compartida en Google Drive del taller cuenta con tres compartimentos claros:

```
📁 Google Drive: Teatro_COAR_Buzon/
│
├── 📥 01_Nuevos_Libretos_Para_Publicar/  <-- Arrastrar nuevos PDFs aquí para publicar
│
├── 🗄️ 02_Libretos_Publicados_En_Web/     <-- Aquí se archivan con sus RECIBOS y enlaces
│
└── 🗑️ 03_Dar_De_Baja_O_Eliminar/         <-- Mover aquí cualquier obra que se quiera retirar
```

---

## 3. Responder a tus dos dudas clave

### Duda 1: ¿Cómo activar la maquinaria sin que Emerson tenga que intervenir?

Tienes **tres alternativas complementarias**, lideradas por el nuevo sistema en la nube 100% autónomo:

#### ⚡ Alternativa 1 (La Más Cómoda): Autonomía Total en la Nube con Google Apps Script (0 Clics)
Gracias al script serverless alojado directamente en Google Drive:
1. El script `GoogleAppsScript_BuzonTeatro.js` corre en los servidores de Google cada 5 minutos las 24 horas del día.
2. Cada vez que alguien sube un PDF a `01_Nuevos_Libretos_Para_Publicar` o mueve un archivo a `03_Dar_De_Baja_O_Eliminar`, Google lo detecta y lo envía por API a GitHub Actions en la nube.
3. GitHub Actions analiza el PDF, extrae los personajes, actualiza el catálogo y despliega en GitHub Pages y Vercel en ~60 segundos.
4. **Nadie tiene que hacer nada más que arrastrar el archivo en Google Drive.** No se requiere encender computadoras, ni ejecutar archivos `.bat`, ni abrir GitHub.

#### Alternativa 2: Desde cualquier celular o navegador con el botón "Run workflow" (1 Clic en GitHub)
Cualquier persona a la que Emerson invite como colaborador al repositorio puede activar la actualización sin instalar nada:
1. Abre en el celular o computadora:  
   👉 **https://github.com/tutuhola57-source/teatro-coar-amazonas/actions**
2. En la lista de la izquierda, haz clic en **`Deploy to GitHub Pages & Cloud Sync`**.
3. Verás un botón a la derecha que dice: **`Run workflow`** con un botón azul.
4. Haces clic en **`Run workflow`** y listo. Los servidores gratuitos de GitHub en la nube se encienden, leen los cambios y actualizan la web en 60 segundos.

#### Alternativa 3: Acceso directo local de respaldo en la computadora del profesor
En la computadora personal del profesor asesor o en la máquina de la biblioteca/sala de profesores del COAR:
1. El asesor instala Google Drive para escritorio (para que la carpeta `Teatro_COAR_Buzon` aparezca sincronizada en su explorador de archivos).
2. Se deja en el Escritorio del profesor el archivo:  
   `Publicar_Libretos_Drive.bat`
3. Cada vez que el profesor suelte un PDF en Drive y quiera forzar la sincronización local inmediata, solo le da **doble clic al icono del escritorio**.
4. La ventana se abre sola, procesa el PDF, actualiza la web y se cierra dejándole el recibo en su Drive.

---

### Duda 2: ¿Cómo pueden "bajar" los archivos que ya subieron?

La palabra "bajar" tiene dos significados en el teatro escolar, y ambos están cubiertos:

#### Significado A: Descargar una copia del PDF para imprimir o ensayar
* **Desde la Web Pública:**  
  Cualquier estudiante o profesor entra a la web, va a la sección **Libretos**, y hace clic en **"Descargar Libreto"**.
* **Desde Google Drive:**  
  Dentro de la carpeta `02_Libretos_Publicados_En_Web/` siempre queda una copia de respaldo intacta de todos los PDFs originales que se han publicado, con su respectivo `RECIBO_<obra>.txt` que contiene el enlace directo de descarga.

#### Significado B: "Dar de baja" / Despublicar / Eliminar una obra si hubo un error
Si el profesor subió una obra por error, con datos incompletos o desea retirarla de la cartelera:

**Método Sencillo desde Google Drive (Sin tocar código):**
1. Entra a Google Drive a la carpeta `02_Libretos_Publicados_En_Web/`.
2. Toma el archivo PDF que deseas retirar y **muévelo a la carpeta `03_Dar_De_Baja_O_Eliminar/`** (o crea un archivo de texto con el nombre de la obra, ej: `baja_fuenteovejuna.txt`).
3. El asistente detecta la solicitud, y automáticamente:
   - **Elimina la obra de la base de datos `obras.json`**.
   - **Borra el PDF del servidor web**.
   - **Reconstruye y publica la web limpia en 60 segundos**.
   - Emite un recibo oficial en Drive: `RECIBO_BAJA_<obra>.txt` confirmando que la obra ya no está visible en internet.

---

## 4. Protocolo de Traspaso Final antes de que Emerson deje el COAR

Antes de graduarte, realiza estos tres pasos administrativos (te tomará menos de 5 minutos):

1. **Compartir la Carpeta de Google Drive:**
   - En Google Drive, haz clic derecho sobre la carpeta `Teatro_COAR_Buzon`.
   - Selecciona **Compartir**.
   - Añade el correo del profesor asesor (ej. correo `@coar.minedu.gob.pe`) con rol de **Editor**.
   - Añade el correo del nuevo estudiante brigadier o delegado de teatro del siguiente grado como Editor de respaldo.

2. **Invitar al Asesor como Colaborador de GitHub:**
   - Entra a: `https://github.com/tutuhola57-source/teatro-coar-amazonas/settings/access`
   - Haz clic en el botón verde **`Add people`**.
   - Escribe el usuario o correo del profesor asesor.
   - El profesor recibirá un correo de invitación gratuito; solo debe aceptar y tendrá permisos para ver el estado del proyecto sin tocar la cuenta personal de Emerson.

3. **Dejar el Enlace Guardado en los Favoritos del Colegio:**
   - Guarda en el navegador de la sala de profesores:
     - Portal Web: `https://tutuhola57-source.github.io/teatro-coar-amazonas/`
     - Carpeta de Drive: Acceso directo a `Teatro_COAR_Buzon`

---

*“Las promociones pasan, pero las obras, la palabra viva y la memoria sobre las tablas de Chachapoyas permanecen.”*  
**Elenco de Teatro • Colegio de Alto Rendimiento (COAR) Amazonas**
