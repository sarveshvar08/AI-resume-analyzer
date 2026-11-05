from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def analyze_resume(resume_text, job_description):

    # Convert text into TF-IDF vectors
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    documents = [resume_text, job_description]

    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate cosine similarity
    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    match_percentage = round(similarity * 100, 2)

    # Extract important terms
    features = vectorizer.get_feature_names_out()

    resume_vector = tfidf_matrix[0].toarray()[0]
    job_vector = tfidf_matrix[1].toarray()[0]

    resume_terms = {
        features[i]
        for i in range(len(features))
        if resume_vector[i] > 0
    }

    job_terms = {
        features[i]
        for i in range(len(features))
        if job_vector[i] > 0
    }

    matching_terms = sorted(resume_terms & job_terms)
    missing_terms = sorted(job_terms - resume_terms)

    return {
        "match_percentage": match_percentage,
        "matching_terms": matching_terms,
        "missing_terms": missing_terms
    }