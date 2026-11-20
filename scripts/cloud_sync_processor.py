#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cloud_sync_processor.py
-----------------------
Headless cloud sync processor for Teatro COAR Amazonas.
Executes both locally and in CI/CD (GitHub Actions Ubuntu runner).

Capabilities:
1. --sync-all: Scans 'public/libretos/*.pdf' against 'src/data/obras.json'.
   Automatically extracts theatrical metadata (title, author, dramatis personae,
   synopsis, staging notes, duration, grade) from any newly added PDF and
   integrates it into the digital catalog.
2. --baja <target>: Unpublishes an obra by ID, slug, or title from 'src/data/obras.json',
   and removes its PDF from 'public/libretos/'.
3. --index-file <file>: Targets a specific PDF inside 'public/libretos/'.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import Counter

# Ensure UTF-8 output across all platforms
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, Exception):
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DATA_JSON = REPO_ROOT / "src" / "data" / "obras.json"
LIBRETOS_DIR = REPO_ROOT / "public" / "libretos"

DEFAULT_COVERS = [
    "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1469488865564-c2de10f69f96?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1514306191717-452ec28c7814?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?auto=format&fit=crop&w=1000&q=80"
]

def clean_slug(text: str) -> str:
    """Normalizes arbitrary text into a clean URL-safe slug."""
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
    """Extracts theatrical catalog metadata from a PDF file."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        
        full_text = ""
        first_pages_text = ""
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            full_text += "\n" + text
            if idx < 4:
                first_pages_text += "\n" + text
    except Exception as e:
        print(f"[WARN] Error reading PDF {pdf_path.name}: {e}")
        num_pages = 1
        full_text = ""
        first_pages_text = ""

    # 1. Título
    titulo = None
    m_title = re.search(r'(?:TÍTULO|OBRA|LIBRETO):\s*([^\n\r]+)', first_pages_text, re.IGNORECASE)
    if m_title:
        titulo = m_title.group(1).strip()
    else:
        # Check first 5 lines for a prominent header line
        lines = [l.strip() for l in first_pages_text.split('\n') if l.strip()]
        for l in lines[:5]:
            if len(l) >= 4 and len(l) <= 60 and not re.search(r'(?:COAR|COLEGIO|MINEDU|MINISTERIO|PÁGINA|ACTO|ESCENA)', l, re.IGNORECASE):
                # If it's all uppercase or prominent title
                if l.isupper() or ":" in l or len(l.split()) <= 8:
                    titulo = l.title() if l.isupper() else l
                    break
        if not titulo:
            raw_name = pdf_path.stem.replace('_', ' ').replace('-', ' ').title()
            titulo = raw_name

    # 2. Autor / Adaptación
    autor = "Elenco de Teatro • COAR Amazonas"
    m_autor = re.search(r'(?:AUTOR|DRAMATURGIA|ADAPTACIÓN|DE|TEXTO DRAMÁTICO BASADO EN):\s*([^\n\r]+)', first_pages_text, re.IGNORECASE)
    if m_autor:
        autor = m_autor.group(1).strip()

    # 3. Duración estimada
    duracion = f"{max(15, num_pages * 3)} min"
    m_dur = re.search(r'(?:DURACIÓN|TIEMPO ESCÉNICO):\s*([^\n\r]+)', first_pages_text, re.IGNORECASE)
    if m_dur:
        duracion = m_dur.group(1).strip()

    # 4. Grado y Año
    anio = str(datetime.now().year)
    m_anio = re.search(r'\b(202[0-9])\b', first_pages_text)
    if m_anio:
        anio = m_anio.group(1)

    grado = "4.° y 5.° de Secundaria"
    m_grado = re.search(r'(\d+[.°º]+\s*(?:y\s*\d+[.°º]+\s*)?(?:Grado|de Secundaria))', first_pages_text, re.IGNORECASE)
    if m_grado:
        grado = m_grado.group(1).strip()

    # 5. Detección de Personajes / Reparto
    reparto = []
    m_reparto_block = re.search(
        r'(?:PERSONAJES|REPARTO|PARTITURAS? VOCALES?|DRAMATIS PERSONAE)[\s\S]*?(?=(?:ACTO|ESCENA|UNIVERSO|PAUTA|GUION|\n\n\n))',
        first_pages_text,
        re.IGNORECASE
    )
    if m_reparto_block:
        block = m_reparto_block.group(0)
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        for l in lines:
            m_p = re.match(r'^(?:[-•*]\s*)?([A-ZÁÉÍÓÚÑ]{3,20})\s*[:\-\—]\s*(.+)$', l)
            if m_p:
                char_name = m_p.group(1).title()
                char_desc = m_p.group(2).strip()
                reparto.append({"personaje": char_name, "actor": char_desc})

    if not reparto and full_text:
        dialogue_chars = re.findall(r'\n\s*([A-ZÁÉÍÓÚÑ]{3,14})\s*\n', full_text)
        common = Counter(dialogue_chars).most_common(10)
        ignored = {'ACTO', 'ESCENA', 'TELON', 'TELÓN', 'AUDIO', 'LUCES', 'PAUSA', 'SILENCIO', 'FINAL', 'INICIO', 'FONDO'}
        for name, count in common:
            if count >= 3 and name not in ignored:
                reparto.append({"personaje": name.title(), "actor": f"Personaje Principal ({name.title()})"})

    if not reparto:
        reparto = [
            {"personaje": "Rol Principal 1", "actor": "Elenco COAR Amazonas"},
            {"personaje": "Rol Principal 2", "actor": "Elenco COAR Amazonas"}
        ]

    # 6. Sinopsis argumental
    sinopsis = None
    m_sin = re.search(r'(?:SINOPSIS|ARGUMENTO|RESUMEN):\s*([^\n\r]+(?:\n[^\n\r]+){1,3})', first_pages_text, re.IGNORECASE)
    if m_sin:
        sinopsis = " ".join(m_sin.group(1).split())
    else:
        sinopsis = (
            f"Puesta en escena y texto dramático de '{titulo}', adaptado y montado por los "
            f"estudiantes del Elenco de Teatro del COAR Amazonas. Libreto íntegro con partitura vocal y "
            f"acotaciones escénicas para ensayos."
        )

    # 7. Género
    genero = "Drama / Creación Colectiva"
    m_gen = re.search(r'(?:GÉNERO):\s*([^\n\r]+)', first_pages_text, re.IGNORECASE)
    if m_gen:
        genero = m_gen.group(1).strip()

    slug = clean_slug(pdf_path.stem)
    try:
        file_size_mb = pdf_path.stat().st_size / (1024 * 1024)
        tamano_str = f"{file_size_mb:.1f} MB" if file_size_mb >= 0.1 else f"{pdf_path.stat().st_size // 1024} KB"
    except Exception:
        tamano_str = f"{num_pages} págs"

    return {
        "id": slug,
        "titulo": titulo,
        "autor": autor,
        "anio": anio,
        "grado": grado,
        "genero": genero,
        "duracion": duracion,
        "sinopsis": sinopsis,
        "portada": DEFAULT_COVERS[0],
        "fotos_escena": DEFAULT_COVERS[:3],
        "pdf_libreto": f"libretos/{pdf_path.name}",
        "pdf_tamano": f"Libreto PDF ({tamano_str})",
        "reparto": reparto,
        "ficha_tecnica": {
            "direccion": "Profesor Asesor • Taller de Teatro COAR Amazonas",
            "luces": "Esquema escolar de reflectores y contraluces",
            "sonido": "Efectos sonoros y musicalización de escena"
        }
    }

def load_data() -> dict:
    if not DATA_JSON.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_JSON}")
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    with open(DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Updated {DATA_JSON.relative_to(REPO_ROOT)}")

def ejecutar_baja(target: str, data: dict) -> bool:
    """Removes an entry from catalog and deletes its PDF if found."""
    target_clean = clean_slug(re.sub(r'^(?:baja|eliminar|quitar)[\-_\s]*', '', target, flags=re.IGNORECASE))
    print(f"[INFO] Processing baja for: '{target}' (clean: '{target_clean}')")
    
    found_obra = None
    for o in data.get("obras", []):
        if o["id"] == target_clean or clean_slug(o["titulo"]) == target_clean or target_clean in o["id"] or target_clean in clean_slug(o["titulo"]):
            found_obra = o
            break

    if not found_obra:
        print(f"[WARN] No catalog entry matched target: '{target}'")
        return False

    print(f"[OK] Removing from catalog: '{found_obra['titulo']}' (id: {found_obra['id']})")
    data["obras"].remove(found_obra)

    # Remove PDF file
    candidate_pdfs = [
        LIBRETOS_DIR / f"{found_obra['id']}.pdf",
        LIBRETOS_DIR / Path(found_obra.get("pdf_libreto", "")).name
    ]
    for p in candidate_pdfs:
        if p.exists() and p.is_file():
            try:
                p.unlink()
                print(f"[OK] Deleted PDF file: {p.name}")
            except Exception as e:
                print(f"[WARN] Could not delete PDF {p.name}: {e}")

    return True

def sync_catalog(data: dict, target_pdf: Path = None) -> bool:
    """Scans public/libretos/*.pdf and ensures every PDF is indexed in obras.json."""
    LIBRETOS_DIR.mkdir(parents=True, exist_ok=True)
    existing_ids = {o["id"]: o for o in data.get("obras", [])}
    existing_pdfs = {Path(o.get("pdf_libreto", "")).name: o for o in data.get("obras", [])}

    if target_pdf:
        pdf_files = [target_pdf] if target_pdf.exists() else []
    else:
        pdf_files = sorted(list(LIBRETOS_DIR.glob("*.pdf")))

    # Legacy demo placeholders that don't need independent auto-indexing
    skipped_placeholders = {"obra-01.pdf", "obra-02.pdf", "obra-03.pdf"}
    changed = False

    for pdf_path in pdf_files:
        if pdf_path.name in skipped_placeholders and ("obra-02" in existing_ids or "obra-03" in existing_ids):
            continue

        slug = clean_slug(pdf_path.stem)
        # Check if already indexed
        if slug in existing_ids or pdf_path.name in existing_pdfs:
            # Already indexed, keep existing
            continue

        print(f"[INFO] New PDF detected without catalog entry: {pdf_path.name}")
        new_meta = extract_metadata_from_pdf(pdf_path)
        data["obras"].insert(0, new_meta)
        existing_ids[new_meta["id"]] = new_meta
        existing_pdfs[pdf_path.name] = new_meta
        print(f"[OK] Indexed new obra: '{new_meta['titulo']}' (id: {new_meta['id']})")
        changed = True

    return changed

def main():
    parser = argparse.ArgumentParser(description="Headless Cloud Sync Processor for Teatro COAR Amazonas")
    parser.add_argument("--sync-all", action="store_true", help="Sync all PDFs in public/libretos/ with obras.json")
    parser.add_argument("--baja", type=str, default="", help="Unpublish an obra by slug, ID, or title")
    parser.add_argument("--index-file", type=str, default="", help="Index a specific PDF file inside public/libretos/")
    args = parser.parse_args()

    data = load_data()
    changed = False

    if args.baja:
        if ejecutar_baja(args.baja, data):
            changed = True

    if args.index_file:
        target = LIBRETOS_DIR / args.index_file
        if target.exists():
            if sync_catalog(data, target_pdf=target):
                changed = True
        else:
            print(f"[ERROR] Target PDF file does not exist: {target}")

    if args.sync_all or (not args.baja and not args.index_file):
        if sync_catalog(data):
            changed = True

    if changed:
        save_data(data)
        print("[SYNC_CHANGED] Changes detected and saved.")
    else:
        print("[NO_CHANGE] Catalog is already synchronized.")

if __name__ == "__main__":
    main()
