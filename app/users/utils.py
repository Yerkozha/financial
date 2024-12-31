# # from PyPDF2 import PdfReader
# # import re
# # import spacy
# # from transformers import AutoTokenizer, AutoModel
import math, random

# # Example: Extract text from a PDF
# def extract_text_from_pdf(book):
#     # Implement logic to extract text from PDF or other formats
#     pass


# def tokenize_text(text):
#     """Tokenize the text into words or sub-words."""
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(text)
#     return [token.text for token in doc]


# def generate_embeddings(tokenized_text):
#     """Generate embeddings using a pre-trained model."""
#     model_name = "bert-base-uncased"
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModel.from_pretrained(model_name)

#     inputs = tokenizer(tokenized_text, return_tensors="pt", padding=True, truncation=True)
#     outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1).tolist()  # Example: Averaging the embeddings


# def extract_text_from_file(file_path):
#     """Extract text from various file formats (PDF, DOCX, etc.)."""
#     try:
#         return PdfReader(file_path).pages[0].extract_text() #.process(file_path).decode('utf-8')
#     except Exception as e:
#         raise ValueError(f"Failed to process file: {e}")

# def process_text_to_json(raw_text):
#     """Convert raw text into structured JSON format (e.g., by paragraphs)."""
#     paragraphs = raw_text.split("\n\n")  # Example: Split by double newlines
#     return {"paragraphs": [{"id": idx, "text": p} for idx, p in enumerate(paragraphs)]}


# import re

# def split_text_into_chapters(raw_text):
#     """
#     Split the raw text into chapters based on specific patterns or delimiters.

#     Args:
#         raw_text (str): The full text of the book.

#     Returns:
#         list: A list of dictionaries, where each dictionary represents a chapter with its title and paragraphs.
#     """
#     # Define a regex pattern for chapter headings (e.g., "Chapter 1", "Chapter I")
#     chapter_pattern = r"(Chapter\s+\d+|Chapter\s+[IVXLCDM]+)"
#     matches = list(re.finditer(chapter_pattern, raw_text))

#     chapters = []
#     for i in range(len(matches)):
#         start_idx = matches[i].start()
#         end_idx = matches[i+1].start() if i+1 < len(matches) else len(raw_text)
#         chapter_text = raw_text[start_idx:end_idx].strip()

#         # Extract chapter title
#         chapter_title_match = re.match(chapter_pattern, chapter_text)
#         chapter_title = chapter_title_match.group(0) if chapter_title_match else f"Chapter {i+1}"

#         # Split chapter into paragraphs
#         paragraphs = [para.strip() for para in chapter_text.split("\n") if para.strip()]

#         chapters.append({
#             "title": chapter_title,
#             "paragraphs": paragraphs
#         })

#     return chapters


# import spacy
# from collections import Counter
# #from nltk.corpus import stopwords

# # Load spaCy model
# nlp = spacy.load("en_core_web_sm")

# def extract_keywords(text, top_n=10):
#     """
#     Extracts keywords from text using NLP techniques.

#     Args:
#         text (str): The text to process.
#         top_n (int): Number of top keywords to return.

#     Returns:
#         list: A list of extracted keywords.
#     """
#     # Process text with spaCy
#     doc = nlp(text)

#     # Filter tokens: keep nouns, adjectives, and proper nouns, exclude stop words and punctuation
#     tokens = [
#         token.text.lower() for token in doc
#         if token.pos_ in {"NOUN", "PROPN", "ADJ"} and not token.is_stop and not token.is_punct
#     ]

#     # Count token frequencies
#     token_counts = Counter(tokens)

#     # Return the top N keywords
#     return [word for word, _ in token_counts.most_common(top_n)]

def generateOTP():
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be changed
    # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP