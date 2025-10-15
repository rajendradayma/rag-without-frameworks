from PyPDF2 import PdfReader

def load_pdf_and_chunk(file, chunk_size=500):
    reader = PdfReader(file)
    all_text = []
    for page in reader.pages:
        try:
            all_text.append(page.extract_text())
        except Exception as e:
            continue
    text = "\n".join([t for t in all_text if t])
    # Simple chunking
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks
