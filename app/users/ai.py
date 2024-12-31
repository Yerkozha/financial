# import textract
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np
# from sentence_transformers import SentenceTransformer
# import json

# from transformers import pipeline
# If users ask for summaries of sections or entire books:
# Use pre-trained models like bart-large-cnn or GPT-based summarizers.
#
# summarizer = pipeline('summarization')
# def summarize_text(text):
#     return summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']


def preprocess_and_embed_book(book):
    print("INSIDE preprocess_and_embed_book !!!")
    print(book)
    # model = SentenceTransformer('all-MiniLM-L6-v2')

    # # Split content into manageable sections
    # sections = book.content  # Assume content is already split into paragraphs or sections
    # embeddings = []
    # for section in sections:
    #     embeddings.append({
    #         'text': section['text'],
    #         'embedding': model.encode(section['text']).tolist()
    #     })

    # # Save embeddings back to the book object
    # book.processed_content.embeddings = embeddings
    # book.processed_content.save()

# def search_book_embeddings(book, query):
#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     query_embedding = model.encode(query)

#     # Find the most similar sections
#     similarities = [
#         (section['text'], cosine_similarity([query_embedding], [section['embedding']])[0][0])
#         for section in book.processed_content.embeddings
#     ]
#     # Sort by similarity
#     similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

#     # Return the top result(s)
#     return similarities[:3]

