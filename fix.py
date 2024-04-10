from PyPDF2 import PdfReader, PdfWriter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Reads each slide once and stores in the dictionary
# This allows:
#   O(n) creation time
#   O(1) fetching time
# Much better compared to reading each time a page is needed
page_dict = {}

def read_pdf(pdf_name):
    reader = PdfReader(pdf_name)
    for i in range(0, len(reader.pages)):
        buffer = reader.pages[i].extract_text()
        page_dict[i] = buffer

def cosine_similarity_matrix(pages):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(pages)
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return similarity_matrix

def fix(pdf_name):
    read_pdf(pdf_name)
    # Using a set avoids the possibility of duplicate pages
    pages_to_remove = set()

    writer = PdfWriter()
    reader = PdfReader(pdf_name)

    pages = list(page_dict.values())
    similarity_matrix = cosine_similarity_matrix(pages)

    for i in range(len(similarity_matrix)):
        for j in range(i + 1, len(similarity_matrix)):
            if similarity_matrix[i][j] > 0.8:
                if len(pages[j]) > len(pages[i]):
                    pages_to_remove.add(i)
                else:
                    pages_to_remove.add(j)

    for i in range(len(reader.pages)):
        if i not in pages_to_remove:
            writer.add_page(reader.pages[i])
    
    fixed_name = pdf_name.replace('.pdf', '_fix.pdf')
    
    with open(fixed_name, "wb") as f:
        writer.write(f)
                