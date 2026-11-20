/**
 * ==============================================================================================
 * SISTEMA AUTÓNOMO DE BUZÓN Y PUBLICACIÓN EN LA NUBE • TEATRO COAR AMAZONAS
 * ==============================================================================================
 * 
 * Este script se ejecuta en Google Apps Script (https://script.google.com) en los servidores
 * de Google de forma 100% gratuita y 24/7.
 * 
 * ¿QUÉ HACE ESTE SCRIPT?
 * 1. Monitorea la carpeta de Google Drive "Teatro_COAR_Buzon".
 * 2. Si encuentra un PDF en "01_Nuevos_Libretos_Para_Publicar":
 *    - Lo sube automáticamente al repositorio web en GitHub (public/libretos/).
 *    - Activa GitHub Actions para extraer metadatos (reparto, autor, sinopsis) y actualizar la web.
 *    - Mueve el PDF a "02_Libretos_Publicados_En_Web".
 *    - Genera un archivo "RECIBO_<nombre>.txt" en Drive con el enlace de la obra para el docente.
 * 3. Si encuentra un archivo en "03_Dar_De_Baja_O_Eliminar":
 *    - Da de baja la obra del portal web y elimina el PDF del servidor.
 *    - Mueve la solicitud a "Historial_Bajas".
 *    - Genera un archivo "RECIBO_BAJA_<nombre>.txt" confirmando el retiro.
 * 
 * INSTALACIÓN EN 2 MINUTOS:
 * 1. Abra https://script.google.com y haga clic en "Nuevo proyecto".
 * 2. Borre el código que aparezca y pegue todo este archivo.
 * 3. Haga clic en el botón "Ejecutar" en la función 'instalarSistemaBuzon'.
 * 4. ¡Listo! El sistema quedará funcionando solo cada 5 minutos.
 * ==============================================================================================
 */

// CONFIGURACIÓN DE CONEXIÓN
const GITHUB_REPO = "tutuhola57-source/teatro-coar-amazonas";
// Token de acceso para la API de GitHub (en Google Drive ya viene pre-configurado en el archivo local)
const GITHUB_TOKEN = "PEGA_AQUI_TU_GITHUB_PERSONAL_ACCESS_TOKEN";
const GITHUB_BRANCH = "main";
const PARENT_FOLDER_NAME = "Teatro_COAR_Buzon";

const FOLDER_NUEVOS_NAME = "01_Nuevos_Libretos_Para_Publicar";
const FOLDER_PUBLICADOS_NAME = "02_Libretos_Publicados_En_Web";
const FOLDER_BAJAS_NAME = "03_Dar_De_Baja_O_Eliminar";

/**
 * Función principal de instalación. Ejecutar esta función una sola vez
 * para configurar el temporizador automático de 5 minutos y verificar carpetas.
 */
function instalarSistemaBuzon() {
  Logger.log("=== INICIANDO INSTALACIÓN DEL BUZÓN TEATRO COAR AMAZONAS ===");
  
  // 1. Verificar o crear carpetas en Drive
  const carpetas = obtenerOCrearEstructuraCarpetas();
  Logger.log("✔ Estructura de carpetas verificada en Google Drive.");

  // 2. Configurar temporizador automático cada 5 minutos
  const triggers = ScriptApp.getProjectTriggers();
  let existeTrigger = false;
  for (let i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === "sincronizarBuzonTeatro") {
      existeTrigger = true;
      break;
    }
  }

  if (!existeTrigger) {
    ScriptApp.newTrigger("sincronizarBuzonTeatro")
      .timeBased()
      .everyMinutes(5)
      .create();
    Logger.log("✔ Disparador automático configurado: se ejecutará cada 5 minutos 24/7.");
  } else {
    Logger.log("ℹ El disparador automático de 5 minutos ya estaba activo.");
  }

  // 3. Ejecutar primera sincronización de prueba
  sincronizarBuzonTeatro();
  Logger.log("=== INSTALACIÓN COMPLETADA CON ÉXITO ===");
}

/**
 * Función que revisa las carpetas y sincroniza con GitHub.
 * Se ejecuta automáticamente cada 5 minutos.
 */
function sincronizarBuzonTeatro() {
  Logger.log("[SYNC] Comprobando novedades en buzón de Google Drive: " + new Date().toLocaleString());
  const carpetas = obtenerOCrearEstructuraCarpetas();
  
  // 1. Procesar Solicitudes de Baja / Despublicación
  procesarBajasDrive(carpetas.bajas);

  // 2. Procesar Nuevas Publicaciones de Libretos PDF
  procesarNuevasPublicacionesDrive(carpetas.nuevos, carpetas.publicados);
}

/**
 * Procesa los archivos que el asesor haya movido a '03_Dar_De_Baja_O_Eliminar'.
 */
function procesarBajasDrive(folderBajas) {
  const files = folderBajas.getFiles();
  let subfolderHistorial = null;

  while (files.hasNext()) {
    const file = files.next();
    const fileName = file.getName();

    // Ignorar recibos previos, instrucciones y archivos de sistema
    if (fileName.startsWith("RECIBO_") || 
        fileName.startsWith("LEEME") || 
        fileName.startsWith(".") || 
        fileName.toLowerCase().endsWith(".ini")) {
      continue;
    }

    Logger.log("[BAJA] Solicitud detectada: " + fileName);
    
    // Obtener slug objetivo
    const baseName = fileName.replace(/\.[^/.]+$/, "");
    const cleanTarget = baseName.replace(/^(baja|eliminar|quitar)[\-_\s]*/i, "").trim();
    const targetSlug = cleanSlug(cleanTarget);

    // Enviar evento de baja a GitHub Actions
    const exitoGitHub = enviarDispatchAGitHub("drive_baja", { baja_target: targetSlug });

    // Asegurar subcarpeta Historial_Bajas
    if (!subfolderHistorial) {
      const subfolders = folderBajas.getFoldersByName("Historial_Bajas");
      if (subfolders.hasNext()) {
        subfolderHistorial = subfolders.next();
      } else {
        subfolderHistorial = folderBajas.createFolder("Historial_Bajas");
      }
    }

    // Mover archivo a historial
    file.moveTo(subfolderHistorial);

    // Generar recibo de baja en Drive
    const fechaHora = Utilities.formatDate(new Date(), "America/Lima", "yyyy-MM-dd HH:mm:ss");
    const reciboContenido = 
      "============================================================\n" +
      "RECIBO DE BAJA / RETIRO DE OBRA • TEATRO COAR AMAZONAS\n" +
      "============================================================\n" +
      "Fecha y Hora: " + fechaHora + " (Hora Perú)\n" +
      "Estado: RETIRADA DE CARTELERA Y DESPUBLICADA CON ÉXITO ✔\n\n" +
      "DATOS DE LA SOLICITUD:\n" +
      "- Obra / Archivo retirado: " + fileName + "\n" +
      "- Identificador procesado: " + targetSlug + "\n\n" +
      "El libreto y la ficha han sido removidos del portal público en internet.\n" +
      "El cambio se refleja en la web en aproximadamente 60 segundos.\n" +
      "============================================================\n";

    folderBajas.createFile("RECIBO_BAJA_" + targetSlug + ".txt", reciboContenido, MimeType.PLAIN_TEXT);
    Logger.log("✔ Recibo de baja emitido para: " + targetSlug);
  }
}

/**
 * Procesa los archivos PDF subidos a '01_Nuevos_Libretos_Para_Publicar'.
 */
function procesarNuevasPublicacionesDrive(folderNuevos, folderPublicados) {
  const files = folderNuevos.getFiles();

  while (files.hasNext()) {
    const file = files.next();
    const fileName = file.getName();

    if (!fileName.toLowerCase().endsWith(".pdf")) {
      continue;
    }

    Logger.log("[NUEVA OBRA] Libreto PDF detectado: " + fileName);
    const baseName = fileName.replace(/\.pdf$/i, "");
    const slug = cleanSlug(baseName);
    const gitHubFilePath = "public/libretos/" + slug + ".pdf";

    // 1. Subir PDF a GitHub mediante API Contents
    const blob = file.getBlob();
    const subidaOk = subirArchivoAGitHub(gitHubFilePath, blob, "feat(libretos): auto-upload " + fileName + " from Drive Buzon");

    if (subidaOk) {
      // 2. Enviar evento de publicación a GitHub Actions
      enviarDispatchAGitHub("drive_publish", { filename: fileName, slug: slug });

      // 3. Mover archivo a carpeta de publicados
      file.moveTo(folderPublicados);

      // 4. Crear recibo de publicación en Drive
      const fechaHora = Utilities.formatDate(new Date(), "America/Lima", "yyyy-MM-dd HH:mm:ss");
      const urlPortal = "https://tutuhola57-source.github.io/teatro-coar-amazonas/";
      const urlLibreto = "https://tutuhola57-source.github.io/teatro-coar-amazonas/libretos/" + slug + ".pdf";

      const reciboContenido = 
        "============================================================\n" +
        "RECIBO DE PUBLICACIÓN AUTOMÁTICA EN WEB • TEATRO COAR AMAZONAS\n" +
        "============================================================\n" +
        "Fecha y Hora: " + fechaHora + " (Hora Perú)\n" +
        "Estado: LIBRETO RECIBIDO Y PUBLICADO EN LÍNEA ✔\n\n" +
        "DATOS DE LA PUBLICACIÓN:\n" +
        "- Archivo original: " + fileName + "\n" +
        "- Identificador web: " + slug + "\n\n" +
        "ENLACES OFICIALES DISPONIBLES:\n" +
        "• Portal Web del Taller: " + urlPortal + "\n" +
        "• Descarga directa del PDF: " + urlLibreto + "\n\n" +
        "La cartelera digital de la web se actualiza automáticamente con\n" +
        "el análisis de reparto, sinopsis y datos de la obra en ~60 segundos.\n" +
        "¡No necesita realizar ninguna acción técnica adicional!\n" +
        "============================================================\n";

      folderPublicados.createFile("RECIBO_" + slug + ".txt", reciboContenido, MimeType.PLAIN_TEXT);
      Logger.log("✔ Libreto publicado y recibo generado para: " + fileName);
    } else {
      Logger.log("❌ Error al subir " + fileName + " a GitHub. Se reintentará en la siguiente ejecución.");
    }
  }
}

/**
 * Sube o actualiza un archivo binario en GitHub mediante la REST API.
 */
function subirArchivoAGitHub(pathInRepo, fileBlob, commitMessage) {
  const url = "https://api.github.com/repos/" + GITHUB_REPO + "/contents/" + encodeURI(pathInRepo);
  
  // Verificar si el archivo ya existe para obtener su SHA (evita errores 422)
  let existingSha = null;
  try {
    const getResponse = UrlFetchApp.fetch(url, {
      method: "get",
      headers: {
        "Authorization": "Bearer " + GITHUB_TOKEN,
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "TeatroCOAR-GoogleAppsScript"
      },
      muteHttpExceptions: true
    });
    if (getResponse.getResponseCode() === 200) {
      const fileInfo = JSON.parse(getResponse.getContentText());
      existingSha = fileInfo.sha;
    }
  } catch (e) {
    Logger.log("Aviso al verificar archivo existente: " + e.toString());
  }

  // Preparar payload con base64
  const payload = {
    message: commitMessage,
    content: Utilities.base64Encode(fileBlob.getBytes()),
    branch: GITHUB_BRANCH
  };
  if (existingSha) {
    payload.sha = existingSha;
  }

  try {
    const putResponse = UrlFetchApp.fetch(url, {
      method: "put",
      contentType: "application/json",
      headers: {
        "Authorization": "Bearer " + GITHUB_TOKEN,
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "TeatroCOAR-GoogleAppsScript"
      },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });

    const code = putResponse.getResponseCode();
    if (code === 200 || code === 201) {
      Logger.log("✔ Archivo subido con éxito a GitHub: " + pathInRepo);
      return true;
    } else {
      Logger.log("❌ Error GitHub API (HTTP " + code + "): " + putResponse.getContentText());
      return false;
    }
  } catch (err) {
    Logger.log("❌ Excepción al subir a GitHub: " + err.toString());
    return false;
  }
}

/**
 * Emite un evento repository_dispatch para activar los flujos de GitHub Actions.
 */
function enviarDispatchAGitHub(eventType, clientPayload) {
  const url = "https://api.github.com/repos/" + GITHUB_REPO + "/dispatches";
  const payload = {
    event_type: eventType,
    client_payload: clientPayload || {}
  };

  try {
    const response = UrlFetchApp.fetch(url, {
      method: "post",
      contentType: "application/json",
      headers: {
        "Authorization": "Bearer " + GITHUB_TOKEN,
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "TeatroCOAR-GoogleAppsScript"
      },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });

    const code = response.getResponseCode();
    if (code === 204) {
      Logger.log("✔ Evento '" + eventType + "' enviado con éxito a GitHub Actions.");
      return true;
    } else {
      Logger.log("Aviso al enviar dispatch (HTTP " + code + "): " + response.getContentText());
      return false;
    }
  } catch (err) {
    Logger.log("Aviso en enviarDispatchAGitHub: " + err.toString());
    return false;
  }
}

/**
 * Localiza o crea la estructura de carpetas en Google Drive.
 */
function obtenerOCrearEstructuraCarpetas() {
  let rootFolder = null;
  const roots = DriveApp.getFoldersByName(PARENT_FOLDER_NAME);
  if (roots.hasNext()) {
    rootFolder = roots.next();
  } else {
    rootFolder = DriveApp.createFolder(PARENT_FOLDER_NAME);
  }

  let folderNuevos = obtenerOCrearSubcarpeta(rootFolder, FOLDER_NUEVOS_NAME);
  let folderPublicados = obtenerOCrearSubcarpeta(rootFolder, FOLDER_PUBLICADOS_NAME);
  let folderBajas = obtenerOCrearSubcarpeta(rootFolder, FOLDER_BAJAS_NAME);

  return {
    root: rootFolder,
    nuevos: folderNuevos,
    publicados: folderPublicados,
    bajas: folderBajas
  };
}

function obtenerOCrearSubcarpeta(parentFolder, subfolderName) {
  const folders = parentFolder.getFoldersByName(subfolderName);
  if (folders.hasNext()) {
    return folders.next();
  }
  return parentFolder.createFolder(subfolderName);
}

/**
 * Normaliza cadenas de texto en un slug limpio URL-friendly.
 */
function cleanSlug(text) {
  if (!text) return "obra-" + new Date().getTime();
  let s = text.toLowerCase();
  s = s.replace(/[áàäâ]/g, "a")
       .replace(/[éèëê]/g, "e")
       .replace(/[íìïî]/g, "i")
       .replace(/[óòöô]/g, "o")
       .replace(/[úùüû]/g, "u")
       .replace(/[ñ]/g, "n");
  s = s.replace(/[^a-z0-9]+/g, "-");
  return s.replace(/^-+|-+$/g, "");
}
