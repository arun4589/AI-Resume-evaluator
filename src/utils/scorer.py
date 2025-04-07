def extract_score(response_text):
    """
    Extract numeric score from model output.
    """
    for line in response_text.split('\n'):
        if "score" in line.lower():
            try:
                score = int(''.join(filter(str.isdigit, line)))
                return score
            except:
                continue
    return 0  # fallback
