def shortlist_candidates(results, threshold=70):
    shortlisted = []
    for result in results:
        try:
            
            if result.score >= threshold:
                name = result.name
                shortlisted.append({"name": name, "score": result.score, "email": result.email,'shortlist_status':"YES"})

            else:
                shortlisted.append({"name": name, "score": result.score, "email": result.email,'shortlist_status':"NO"})    
        except Exception:
            continue
    return shortlisted
