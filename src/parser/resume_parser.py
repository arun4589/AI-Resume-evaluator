from pdfminer.high_level import extract_text

def parse_resume(file):
    return extract_text(file)
