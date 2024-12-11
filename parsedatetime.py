import re
from datetime import datetime
import parsedatetime

# Initialize parsedatetime Calendar
cal = parsedatetime.Calendar()

def clean_text(text):
    """
    Cleans and standardizes text by removing unnecessary formatting and converting to lowercase.
    Args:
        text (str): Input text to clean.
    Returns:
        str: Cleaned and standardized text.
    """
    # Remove list formatting, excessive whitespace, and convert to lowercase
    text = re.sub(r"\d\.\s+|[a-z]\)\s+|•\s+|[A-Z]\.\s+|[IVX]+\.\s+", " ", text)
    text = re.sub(r" +", " ", text)
    return text.lower()

def process_single_note(clean_notes, note_datetime):
    """
    Processes a single clinical note to extract and match datetime expressions.
    Args:
        clean_notes (str): Cleaned clinical note text.
        note_datetime (str): The datetime of the note in "%Y-%m-%d %H:%M:%S" format.
    """
    # Clean the input text
    cleaned_text = clean_text(clean_notes)

    # Parse the input datetime
    reference_date = datetime.strptime(str(note_datetime), "%Y-%m-%d %H:%M:%S")

    # Use parsedatetime to detect datetime expressions
    date_results = cal.nlp(cleaned_text, reference_date)

    print("Input Text:")
    print(cleaned_text)
    print("\nDetected Datetime Expressions:")

    # Split text into sentences and store indices
    sentences = cleaned_text.split(".")
    sentences_with_indices = []
    for sentence in sentences:
        if sentence.strip():  # Avoid empty sentences
            sentences_with_indices.append((sentence, cleaned_text.index(sentence)))

    # Process each detected datetime
    for result in date_results or []:
        # Skip if the detected datetime is not in the same year as the reference date
        if result[0].year != reference_date.year:
            continue

        # Identify the sentence containing the datetime expression
        detected_sentence = None
        for sentence, index in sentences_with_indices:
            if result[2] < index:
                break
            detected_sentence = sentence

        # Check for the keyword "pain" in the detected sentence
        if detected_sentence and "pain" in detected_sentence:
            detected_time = result[0].strftime("%m/%d/%Y %H:%M:%S")
            print(f"Sentence: {detected_sentence.strip()}")
            print(f"Phrase: {result[4].strip()}")
            print(f"Time Detected: {detected_time}\n")

# Example usage
if __name__ == "__main__":
    # Example input
    example_clean_notes = "c/o midsternal chest pain radiating to right arm and neck since 0530 today."
    example_note_datetime = "2018-01-12 13:12:00"

    # Process the single note
    process_single_note(example_clean_notes, example_note_datetime)
