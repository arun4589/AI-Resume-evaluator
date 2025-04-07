from pdfminer.high_level import extract_text

def parse_jd(file):
    return extract_text(file)
