from celery import shared_task
from transformers import pipeline
from .models import Book, Chapter, AIInsights, ProcessedContent, Paragraph
from .utils import extract_text_from_pdf, tokenize_text, generate_embeddings, split_text_into_chapters, extract_keywords

# Load pre-trained NLP models (Hugging Face)
summarizer = pipeline("summarization")
sentiment_analyzer = pipeline("sentiment-analysis")
tokenizer = pipeline("feature-extraction")  # Tokenization for embedding generation


@shared_task
def process_book_content(book_id):
    """Process book content, generate insights, and store them in the database."""
    try:
        book = Book.objects.get(id=book_id)

        # Step 1: Extract raw text from the uploaded file (PDF, DOCX, etc.)
        raw_text = extract_text_from_pdf(book)  # Implement this utility function for file parsing

        # Step 2: Split the content into chapters and paragraphs
        chapters = split_text_into_chapters(raw_text)  # Define how to split text into chapters and paragraphs
        for idx, chapter in enumerate(chapters):
            Chapter.objects.create(book=book, title=f"Chapter {idx + 1}", order=idx, content=chapter['text'])
            for p_idx, paragraph in enumerate(chapter['paragraphs']):
                Paragraph.objects.create(chapter=chapter, order=p_idx, text=paragraph)

        # Step 3: Perform AI processing (summarization, sentiment analysis, etc.)
        summary = summarizer(raw_text)
        sentiment = sentiment_analyzer(raw_text)
        keywords = extract_keywords(raw_text)  # Define this function for keyword extraction

        # Step 4: Save AI insights to the database
        AIInsights.objects.create(
            book=book,
            summary=summary[0]['summary_text'],
            sentiment=sentiment,
            keywords=keywords
        )

        # Step 5: Tokenize text and generate embeddings for future ML tasks
        tokenized_text = tokenize_text(raw_text)  # Implement the tokenization logic
        embeddings = generate_embeddings(tokenized_text)  # Implement embedding generation using your chosen model
        ProcessedContent.objects.create(
            book=book,
            tokenized=tokenized_text,
            embeddings=embeddings
        )

    except Exception as e:
        print(f"Error processing book {book_id}: {e}")


