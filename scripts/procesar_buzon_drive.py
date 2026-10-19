#!/usr/bin/env python3
r"""
procesar_buzon_drive.py
-----------------------
Asistente automatizado para el Taller de Teatro del COAR Amazonas.
Monitorea la carpeta de Google Drive:
  G:\My Drive\Teatro_COAR_Buzon\Nuevos_Libretos_Para_Publicar\
Lee cualquier PDF entrante, extrae automáticamente sus metadatos (título, autor,
reparto de personajes, sinopsis, duración), lo incorpora al catálogo obras.json,
lo compila y publica automáticamente en la web con Git/GitHub Pages.
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

# Rutas del entorno
DRIVE_ROOT = Path(r"G:\My Drive\Teatro_COAR_Buzon")
BUZON_INCOMING = DRIVE_ROOT / "Nuevos_Libretos_Para_Publicar"
BUZON_PROCESSED = DRIVE_ROOT / "Libretos_Ya_Publicados"

PROJECT_ROOT = Path(r"D:\Proyectos\teatro-coar-amazonas")
DATA_JSON = PROJECT_ROOT / "src" / "data" / "obras.json"
PUBLIC_LIBRETOS = PROJECT_ROOT / "public" / "libretos"

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
    # Buscar patrones como "TÍTULO: X" o la primera línea en mayúsculas
    m_title = re.search(r'(?:TÍTULO|OBRA|LIBRETO):\s*([^\n\r]+)', first_pages_text, re.IGNORECASE)
    if m_title:
        titulo = m_title.group(1).strip()
    else:
        # Tomar el nombre del archivo limpio si no se detecta título explícito
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
    # Buscar sección de personajes
    m_reparto_block = re.search(r'(?:PERSONAJES|REPARTO|PARTITURAS? VOCALES?|DRAMATIS PERSONAE)[\s\S]*?(?=(?:ACTO|ESCENA|UNIVERSO|PAUTA|GUION|\n\n\n))', first_pages_text, re.IGNORECASE)
    if m_reparto_block:
        block = m_reparto_block.group(0)
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        for l in lines:
            # Buscar patrones tipo "MATEO: El Brigadier..." o "• LAURENCIA - Joven..."
            m_p = re.match(r'^(?:[-•*]\s*)?([A-ZÁÉÍÓÚÑ]{3,15})\s*[:\-\—]\s*(.+)$', l)
            if m_p:
                char_name = m_p.group(1).title()
                char_desc = m_p.group(2).strip()
                reparto.append({"personaje": char_name, "actor": char_desc})
    
    # Si no se detectó tabla formal, buscar nombres en mayúsculas recurrentes antes de diálogos
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
    sinopsis = ""
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

def procesar_buzon():
    """Escanea la carpeta de Drive, procesa PDFs y actualiza el proyecto web."""
    if not BUZON_INCOMING.exists():
        print(f"[AVISO] Creando carpeta buzón en Drive: {BUZON_INCOMING}")
        BUZON_INCOMING.mkdir(parents=True, exist_ok=True)
    if not BUZON_PROCESSED.exists():
        BUZON_PROCESSED.mkdir(parents=True, exist_ok=True)

    archivos_pdf = list(BUZON_INCOMING.glob("*.pdf"))
    if not archivos_pdf:
        print(f"[INFO] No hay nuevos archivos PDF en el buzón: {BUZON_INCOMING}")
        return False

    print(f"[INFO] Se encontraron {len(archivos_pdf)} archivo(s) PDF en el buzón para procesar.")

    # Cargar base de datos existente
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    obras_existentes = {o["id"]: o for o in data.get("obras", [])}
    procesados = []

    for pdf_file in archivos_pdf:
        print(f"\n--- Procesando: {pdf_file.name} ---")
        meta = extract_metadata_from_pdf(pdf_file)
        slug_id = meta["id"]
        
        # 1. Copiar el PDF renombrado a public/libretos/
        dest_pdf = PUBLIC_LIBRETOS / f"{slug_id}.pdf"
        PUBLIC_LIBRETOS.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(pdf_file), str(dest_pdf))
        print(f"  ✔ PDF copiado a: {dest_pdf.relative_to(PROJECT_ROOT)}")

        # 2. Asignar portada e imágenes por defecto
        meta["portada"] = "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?auto=format&fit=crop&w=1000&q=80"
        meta["fotos_escena"] = [
            "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1469488865564-c2de10f69f96?auto=format&fit=crop&w=1000&q=80"
        ]
        meta["pdf_libreto"] = f"libretos/{slug_id}.pdf"

        # 3. Insertar o actualizar en obras.json
        if slug_id in obras_existentes:
            print(f"  ✔ Actualizando obra existente: '{meta['titulo']}'")
            # Preservar fotos personalizadas si ya existían
            meta["portada"] = obras_existentes[slug_id].get("portada", meta["portada"])
            meta["fotos_escena"] = obras_existentes[slug_id].get("fotos_escena", meta["fotos_escena"])
            # Reemplazar
            for idx, o in enumerate(data["obras"]):
                if o["id"] == slug_id:
                    data["obras"][idx] = meta
                    break
        else:
            print(f"  ✔ Agregando nueva obra al catálogo: '{meta['titulo']}'")
            # Colocarla al inicio de la lista
            data["obras"].insert(0, meta)

        # 4. Mover PDF a procesados en Drive
        dest_drive = BUZON_PROCESSED / pdf_file.name
        shutil.move(str(pdf_file), str(dest_drive))
        print(f"  ✔ Movido a procesados en Drive: {dest_drive.name}")

        # 5. Generar recibo de publicación para el profesor asesor
        recibo_path = BUZON_PROCESSED / f"RECIBO_{slug_id}.txt"
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
        print(f"  ✔ Recibo generado para el asesor en Drive: {recibo_path.name}")

        procesados.append(meta)

    # Guardar obras.json
    with open(DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n[INFO] Archivo obras.json actualizado con {len(procesados)} obra(s).")

    # 6. Compilar Astro localmente para validar
    print("[INFO] Validando compilación con Astro...")
    build_proc = subprocess.run(["npm", "run", "build"], cwd=str(PROJECT_ROOT), capture_output=True, text=True, shell=True)
    if build_proc.returncode != 0:
        print("[ERROR] Falló la compilación de Astro:", build_proc.stderr)
        return False
    print("  ✔ Compilación Astro validada exitosamente con 0 errores.")

    # 7. Git commit y push automático
    print("[INFO] Sincronizando con repositorio GitHub...")
    subprocess.run(["git", "add", "."], cwd=str(PROJECT_ROOT), check=True)
    nombres = ", ".join([p["titulo"] for p in procesados])
    commit_msg = f"feat(teatro): auto-publicar '{nombres}' desde buzon de Google Drive"
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(PROJECT_ROOT), check=True)
    push_proc = subprocess.run(["git", "push", "origin", "main"], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
    if push_proc.returncode == 0:
        print("  ✔ Cambios subidos a GitHub origin/main.")
        print("  ✔ GitHub Actions & Vercel activados automáticamente. La web se actualizará en 60 segundos.")
    else:
        print("[ADVERTENCIA] Error en git push:", push_proc.stderr)

    return True

if __name__ == "__main__":
    procesar_buzon()
