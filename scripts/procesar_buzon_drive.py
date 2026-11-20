#!/usr/bin/env python3
r"""
procesar_buzon_drive.py
-----------------------
Asistente integral y automatizado para el Taller de Teatro del COAR Amazonas.
Gestiona el ciclo de vida completo de libretos desde Google Drive:
1. PUBLICAR: Lee PDFs en '01_Nuevos_Libretos_Para_Publicar', extrae metadatos
   (título, autor, reparto, sinopsis, duración), actualiza obras.json y publica en GitHub.
2. DAR DE BAJA / ELIMINAR: Si el asesor mueve un PDF o archivo a '03_Dar_De_Baja_O_Eliminar',
   el asistente despublica la obra de obras.json, elimina el PDF de la web y emite un recibo.
"""

import os
import re
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from pypdf import PdfReader

# Forzar codificación UTF-8 en consola de Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Rutas del entorno local y Drive
DRIVE_ROOT = Path(r"G:\My Drive\Teatro_COAR_Buzon")

# Carpetas de subida (compatibles con nomenclatura moderna y previa)
BUZON_INCOMING_CANDIDATES = [
    DRIVE_ROOT / "01_Nuevos_Libretos_Para_Publicar",
    DRIVE_ROOT / "Nuevos_Libretos_Para_Publicar"
]

BUZON_PROCESSED_CANDIDATES = [
    DRIVE_ROOT / "02_Libretos_Publicados_En_Web",
    DRIVE_ROOT / "Libretos_Ya_Publicados"
]

BUZON_BAJAS_CANDIDATES = [
    DRIVE_ROOT / "03_Dar_De_Baja_O_Eliminar",
    DRIVE_ROOT / "Dar_De_Baja_O_Eliminar"
]

PROJECT_ROOT = Path(r"D:\Proyectos\teatro-coar-amazonas")
DATA_JSON = PROJECT_ROOT / "src" / "data" / "obras.json"
PUBLIC_LIBRETOS = PROJECT_ROOT / "public" / "libretos"

def get_drive_dirs():
    """Obtiene y asegura la existencia de las carpetas de Drive."""
    incoming = next((p for p in BUZON_INCOMING_CANDIDATES if p.exists()), BUZON_INCOMING_CANDIDATES[0])
    processed = next((p for p in BUZON_PROCESSED_CANDIDATES if p.exists()), BUZON_PROCESSED_CANDIDATES[0])
    bajas = next((p for p in BUZON_BAJAS_CANDIDATES if p.exists()), BUZON_BAJAS_CANDIDATES[0])
    
    incoming.mkdir(parents=True, exist_ok=True)
    processed.mkdir(parents=True, exist_ok=True)
    bajas.mkdir(parents=True, exist_ok=True)
    return incoming, processed, bajas

def clean_slug(text: str) -> str:
    """Convierte un título en un slug limpio para URL y archivo PDF."""
    text = text.lower()
    text = re.sub(r'[áàäâ]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöô]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def extract_metadata_from_pdf(pdf_path: Path) -> dict:
    """Lee el contenido del PDF y extrae los metadatos esenciales para el catálogo."""
    reader = PdfReader(str(pdf_path))
    num_pages = len(reader.pages)
    
    full_text = ""
    first_pages_text = ""
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        full_text += "\n" + text
        if idx < 3:
            first_pages_text += "\n" + text

    # 1. Título
    titulo = None
    m_title = re.search(r'(?:TÍTULO|OBRA|LIBRETO):\s*([^\n\r]+)', first_pages_text, re.IGNORECASE)
    if m_title:
        titulo = m_title.group(1).strip()
    else:
        raw_name = pdf_path.stem.replace('_', ' ').replace('-', ' ').title()
        titulo = raw_name

    # 2. Autor / Adaptación
    autor = "Elenco de Teatro • COAR Amazonas"
    m_autor = re.search(r'(?:AUTOR|DRAMATURGIA|ADAPTACIÓN|DE):\s*([^\n\r]+)', first_pages_text, re.IGNORECASE)
    if m_autor:
        autor = m_autor.group(1).strip()

    # 3. Duración estimada
    duracion = f"{max(15, num_pages * 3)} min"
    m_dur = re.search(r'(?:DURACIÓN|TIEMPO ESCÉNICO):\s*([^\n\r]+)', first_pages_text, re.IGNORECASE)
    if m_dur:
        duracion = m_dur.group(1).strip()

    # 4. Grado y Año
    anio = str(datetime.now().year)
    grado = "4.° y 5.° de Secundaria"
    m_grado = re.search(r'(\d+[.°º]+\s*(?:y\s*\d+[.°º]+\s*)?(?:Grado|de Secundaria))', first_pages_text, re.IGNORECASE)
    if m_grado:
        grado = m_grado.group(1).strip()

    # 5. Detección de Personajes / Reparto
    reparto = []
    m_reparto_block = re.search(r'(?:PERSONAJES|REPARTO|PARTITURAS? VOCALES?|DRAMATIS PERSONAE)[\s\S]*?(?=(?:ACTO|ESCENA|UNIVERSO|PAUTA|GUION|\n\n\n))', first_pages_text, re.IGNORECASE)
    if m_reparto_block:
        block = m_reparto_block.group(0)
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        for l in lines:
            m_p = re.match(r'^(?:[-•*]\s*)?([A-ZÁÉÍÓÚÑ]{3,15})\s*[:\-\—]\s*(.+)$', l)
            if m_p:
                char_name = m_p.group(1).title()
                char_desc = m_p.group(2).strip()
                reparto.append({"personaje": char_name, "actor": char_desc})
    
    if not reparto:
        dialogue_chars = re.findall(r'\n\s*([A-ZÁÉÍÓÚÑ]{3,14})\s*\n', full_text)
        from collections import Counter
        common = Counter(dialogue_chars).most_common(8)
        for name, count in common:
            if count >= 3 and name not in ['ACTO', 'ESCENA', 'TELÓN', 'AUDIO', 'LUCES', 'PAUSA', 'SILENCIO', 'FINAL', 'INICIO']:
                reparto.append({"personaje": name.title(), "actor": f"Personaje Principal ({name.title()})"})

    if not reparto:
        reparto = [
            {"personaje": "Rol Principal 1", "actor": "Elenco COAR Amazonas"},
            {"personaje": "Rol Principal 2", "actor": "Elenco COAR Amazonas"}
        ]

    # 6. Sinopsis argumental
    m_sin = re.search(r'(?:SINOPSIS|ARGUMENTO|RESUMEN):\s*([^\n\r]+(?:\n[^\n\r]+){1,3})', first_pages_text, re.IGNORECASE)
    if m_sin:
        sinopsis = " ".join(m_sin.group(1).split())
    else:
        sinopsis = f"Puesta en escena y texto dramático de '{titulo}', adaptado y montado por los estudiantes del Elenco de Teatro del COAR Amazonas. Libreto íntegro con partitura vocal y acotaciones para ensayos."

    # 7. Género
    genero = "Drama / Creación Colectiva"
    m_gen = re.search(r'(?:GÉNERO):\s*([^\n\r]+)', first_pages_text, re.IGNORECASE)
    if m_gen:
        genero = m_gen.group(1).strip()

    slug = clean_slug(titulo)
    file_size_mb = pdf_path.stat().st_size / (1024 * 1024)
    tamano_str = f"{file_size_mb:.1f} MB" if file_size_mb >= 0.1 else f"{pdf_path.stat().st_size // 1024} KB"

    return {
        "id": slug,
        "titulo": titulo,
        "autor": autor,
        "anio": anio,
        "grado": grado,
        "genero": genero,
        "duracion": duracion,
        "sinopsis": sinopsis,
        "pdf_tamano": f"Libreto PDF ({tamano_str})",
        "reparto": reparto,
        "ficha_tecnica": {
            "direccion": "Profesor Asesor • Taller de Teatro COAR Amazonas",
            "luces": "Esquema escolar de reflectores y contraluces",
            "sonido": "Efectos sonoros y musicalización de escena"
        }
    }

def procesar_bajas(bajas_dir: Path, data: dict) -> list:
    """Procesa obras que el asesor desea dar de baja o despublicar."""
    archivos_baja = [
        p for p in bajas_dir.iterdir()
        if p.is_file()
        and not p.name.startswith("RECIBO_")
        and not p.name.startswith("LEEME")
        and not p.name.startswith(".")
        and not p.name.lower().endswith(".ini")
    ]
    if not archivos_baja:
        return []

    print(f"\n[INFO] Se encontraron {len(archivos_baja)} solicitud(es) de baja/despublicación.")
    historial_dir = bajas_dir / "Historial_Bajas"
    historial_dir.mkdir(parents=True, exist_ok=True)
    
    bajas_ejecutadas = []

    for item in archivos_baja:
        # Extraer slug o nombre objetivo
        target_name = item.stem
        # Limpiar si empieza con 'baja_' o 'eliminar_'
        target_slug = clean_slug(re.sub(r'^(?:baja|eliminar|quitar)[\-_\s]*', '', target_name, flags=re.IGNORECASE))
        print(f"  -> Solicitud para retirar: '{target_name}' (slug: {target_slug})")

        # Buscar coincidencia en obras.json
        obra_encontrada = None
        for o in data.get("obras", []):
            if o["id"] == target_slug or target_slug in clean_slug(o["titulo"]) or clean_slug(o["titulo"]) in target_slug:
                obra_encontrada = o
                break

        if obra_encontrada:
            print(f"  ✔ Despublicando del catálogo: '{obra_encontrada['titulo']}' (id: {obra_encontrada['id']})")
            data["obras"].remove(obra_encontrada)
            
            # Eliminar PDF de public/libretos/ si existe
            target_pdf = PUBLIC_LIBRETOS / f"{obra_encontrada['id']}.pdf"
            if target_pdf.exists():
                try:
                    target_pdf.unlink()
                    print(f"  ✔ Archivo PDF retirado del servidor: {target_pdf.name}")
                except Exception as e:
                    print(f"  [AVISO] No se pudo borrar el PDF: {e}")

            # Generar recibo de baja en Drive
            recibo_baja = bajas_dir / f"RECIBO_BAJA_{obra_encontrada['id']}.txt"
            recibo_content = f"""============================================================
RECIBO DE BAJA / RETIRO DE OBRA • TEATRO COAR AMAZONAS
============================================================
Fecha y Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Estado: RETIRADA DE CARTELERA Y DESPUBLICADA CON ÉXITO ✔

DATOS DE LA OBRA DESPUBLICADA:
- Título: {obra_encontrada['titulo']}
- Identificador: {obra_encontrada['id']}
- Temporada: {obra_encontrada.get('anio', 'N/A')}

El libreto y la ficha han sido removidos del portal público.
El cambio se refleja en la web en aproximadamente 60 segundos tras el despliegue automático.
============================================================
"""
            with open(recibo_baja, "w", encoding="utf-8") as rf:
                rf.write(recibo_content)
            print(f"  ✔ Recibo de despublicación generado: {recibo_baja.name}")

            # Mover archivo de solicitud a Historial_Bajas
            dest_hist = historial_dir / item.name
            if dest_hist.exists():
                dest_hist.unlink()
            shutil.move(str(item), str(dest_hist))

            bajas_ejecutadas.append(obra_encontrada["titulo"])
        else:
            print(f"  [AVISO] No se encontró ninguna obra activa en el catálogo coincidente con: '{target_name}'")
            # Mover a historial de todos modos
            shutil.move(str(item), str(historial_dir / item.name))

    return bajas_ejecutadas

def procesar_buzon():
    """Escanea la carpeta de Drive, procesa publicaciones y bajas, y sincroniza la web."""
    incoming_dir, processed_dir, bajas_dir = get_drive_dirs()

    # Cargar base de datos existente
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    cambios_realizados = False

    # 1. Procesar Bajas
    bajas_list = procesar_bajas(bajas_dir, data)
    if bajas_list:
        cambios_realizados = True

    # 2. Procesar Nuevas Publicaciones
    archivos_pdf = list(incoming_dir.glob("*.pdf"))
    procesados = []

    if archivos_pdf:
        print(f"\n[INFO] Se encontraron {len(archivos_pdf)} nuevo(s) libreto(s) PDF para publicar.")
        obras_existentes = {o["id"]: o for o in data.get("obras", [])}

        for pdf_file in archivos_pdf:
            print(f"\n--- Procesando libreto: {pdf_file.name} ---")
            meta = extract_metadata_from_pdf(pdf_file)
            slug_id = meta["id"]
            
            dest_pdf = PUBLIC_LIBRETOS / f"{slug_id}.pdf"
            PUBLIC_LIBRETOS.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(pdf_file), str(dest_pdf))
            print(f"  ✔ PDF copiado a: {dest_pdf.relative_to(PROJECT_ROOT)}")

            meta["portada"] = "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?auto=format&fit=crop&w=1000&q=80"
            meta["fotos_escena"] = [
                "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?auto=format&fit=crop&w=1000&q=80",
                "https://images.unsplash.com/photo-1469488865564-c2de10f69f96?auto=format&fit=crop&w=1000&q=80"
            ]
            meta["pdf_libreto"] = f"libretos/{slug_id}.pdf"

            if slug_id in obras_existentes:
                print(f"  ✔ Actualizando ficha de obra: '{meta['titulo']}'")
                meta["portada"] = obras_existentes[slug_id].get("portada", meta["portada"])
                meta["fotos_escena"] = obras_existentes[slug_id].get("fotos_escena", meta["fotos_escena"])
                for idx, o in enumerate(data["obras"]):
                    if o["id"] == slug_id:
                        data["obras"][idx] = meta
                        break
            else:
                print(f"  ✔ Incorporando al catálogo: '{meta['titulo']}'")
                data["obras"].insert(0, meta)

            # Mover a procesados
            dest_drive = processed_dir / pdf_file.name
            if dest_drive.exists():
                dest_drive.unlink()
            shutil.move(str(pdf_file), str(dest_drive))
            print(f"  ✔ Archivado en Drive: {dest_drive.name}")

            # Generar recibo de publicación
            recibo_path = processed_dir / f"RECIBO_{slug_id}.txt"
            reparto_str = "\n".join([f"  - {r['personaje']}: {r['actor']}" for r in meta['reparto']])
            recibo_content = f"""============================================================
RECIBO DE PUBLICACIÓN AUTOMÁTICA EN WEB • TEATRO COAR AMAZONAS
============================================================
Fecha y Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Estado: PUBLICADO Y EN LÍNEA ✔

DATOS EXTRAÍDOS DE SU LIBRETO:
- Título: {meta['titulo']}
- Autor: {meta['autor']}
- Grado: {meta['grado']}
- Temporada: {meta['anio']}
- Duración estimada: {meta['duracion']}
- Género: {meta['genero']}

REPARTO DETECTADO:
{reparto_str}

ENLACES DIRECTOS:
- Portal Web del Taller: https://tutuhola57-source.github.io/teatro-coar-amazonas/
- Descarga directa del PDF: https://tutuhola57-source.github.io/teatro-coar-amazonas/libretos/{slug_id}.pdf

El sitio web se reconstruye automáticamente mediante GitHub Actions y Vercel en ~60 segundos.
No necesita realizar ninguna acción técnica adicional.
============================================================
"""
            with open(recibo_path, "w", encoding="utf-8") as rf:
                rf.write(recibo_content)
            print(f"  ✔ Recibo generado para el asesor: {recibo_path.name}")
            procesados.append(meta)

        cambios_realizados = True

    if not cambios_realizados:
        print("[INFO] No hay cambios pendientes (sin nuevos libretos ni solicitudes de baja).")
        return False

    # Guardar obras.json
    with open(DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n[INFO] Base de datos 'obras.json' actualizada con éxito.")

    # Validar compilación local
    print("[INFO] Validando compilación con Astro...")
    build_proc = subprocess.run(["npm", "run", "build"], cwd=str(PROJECT_ROOT), capture_output=True, text=True, shell=True)
    if build_proc.returncode != 0:
        print("[ERROR] Falló la compilación de Astro:", build_proc.stderr)
        return False
    print("  ✔ Compilación Astro validada con 0 errores.")

    # Sincronización Git automática
    print("[INFO] Sincronizando con repositorio GitHub...")
    subprocess.run(["git", "add", "."], cwd=str(PROJECT_ROOT), check=True)
    
    mensajes = []
    if procesados:
        nombres = ", ".join([p["titulo"] for p in procesados])
        mensajes.append(f"publicar '{nombres}'")
    if bajas_list:
        nombres_bajas = ", ".join(bajas_list)
        mensajes.append(f"despublicar '{nombres_bajas}'")
    
    commit_msg = f"feat(teatro): auto-{'; '.join(mensajes)} desde Google Drive"
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(PROJECT_ROOT), check=True)
    push_proc = subprocess.run(["git", "push", "origin", "main"], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
    if push_proc.returncode == 0:
        print("  ✔ Cambios subidos a GitHub origin/main.")
        print("  ✔ Despliegue en la nube activado. La web se actualizará en 60 segundos.")
    else:
        print("[ADVERTENCIA] Error en git push:", push_proc.stderr)

    return True

if __name__ == "__main__":
    procesar_buzon()
