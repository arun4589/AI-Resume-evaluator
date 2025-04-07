def shortlist_candidates(results, threshold=70):
    shortlisted = []
    for result in results:
        try:
            score_line = [line for line in result.split('\n') if 'Score' in line][0]
            score = int(''.join(filter(str.isdigit, score_line)))
            if score >= threshold:
                name = [line for line in result.split('\n') if 'Name' in line][0].split(":")[-1].strip()
                shortlisted.append({"name": name, "score": score, "summary": result})
        except Exception:
            continue
    return shortlisted
