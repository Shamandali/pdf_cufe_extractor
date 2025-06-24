Extractor de CUFE desde PDFs

Crear y activar el entorno
python3 -m venv env
source env/bin/activate

Dependencias
pip install PyMuPDF

Ejecución
python main.py

Problema identificado
El regex proporcionado en la especificación original:
REGEX_CUFE = r'\b([0-9a-fA-F]{95,100})\b'
No funciona correctamente con PDFs porque el CUFE formateado tiene espacios y saltos de línea

Solución implementada
Se utiliza un regex más flexible adicional:
REGEX_CUFE_AJUSTADO = r'\b([0-9a-fA-F\s\n]{95,200})\b'
Que permite Espacios (\s) entre caracteres hexadecimales y saltos de línea (\n)

**Por efectos de legibilidad en pruebas se usa la función clear_database() para limpiar todos los registros**
💾 La base de datos `facturas.db` se crea automáticamente al ejecutar el script `main.py`.
Las facturas deben estar en una carpeta`invoice`.
