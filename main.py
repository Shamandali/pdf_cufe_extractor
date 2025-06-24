import fitz
import re
import os
import sqlite3

DB_FILE = "facturas.db"
PDF_DIR = "invoice"  
REGEX_CUFE = r'\b([0-9a-fA-F]{95,100})\b'
REGEX_CUFE_AJUSTADO = r'\b([0-9a-fA-F\s\n]{95,200})\b'  # permite espacios y saltos de línea

def extract_cufe_from_pdf(filepath):
    try:
        with fitz.open(filepath) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            
            pages = len(doc)
            size = os.path.getsize(filepath)

        matches_original = re.findall(REGEX_CUFE, text)
        
        for match in matches_original:
            if 95 <= len(match) <= 100:
                return match, pages, size
        
        matches2 = re.findall(REGEX_CUFE_AJUSTADO, text)
        
        for i, match in enumerate(matches2):
            cufe_clean = re.sub(r'[^0-9a-fA-F]', '', match)
            if 95 <= len(cufe_clean) <= 100:
                return cufe_clean, pages, size
        
    except Exception as e:
        print(f"Error procesando {filepath}: {e}")
        return None, 0, 0

def create_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            pages INTEGER,
            cufe TEXT,
            size INTEGER
        )
    ''')
    conn.commit()
    return conn

def clear_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM facturas")
    conn.commit()
    count = cursor.rowcount
    conn.close()
    print(f"✅ Se borraron {count} registros de la base de datos")
    return count

def main():

    conn = create_db()
    cursor = conn.cursor()

    for filename in os.listdir(PDF_DIR):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(PDF_DIR, filename)
            cufe, pages, size = extract_cufe_from_pdf(filepath)
            
            cursor.execute('''
                INSERT INTO facturas (filename, pages, cufe, size)
                VALUES (?, ?, ?, ?)
                ''', (filename, pages, cufe or "Not found", size))

    conn.commit()
    cursor.execute("SELECT * FROM facturas")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Archivo: {row[1]}, Páginas: {row[2]}, CUFE: {row[3][:20]}..., Tamaño: {row[4]} bytes")
    
    conn.close()        
if __name__ == "__main__":
    #clear_database() // Descomentar para limpiar la base de datos
    main()