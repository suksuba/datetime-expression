import pandas as pd
import re
from datetime import datetime, timedelta
import parsedatetime

# Function to clean text (basic lowercase conversion)
def clean_text(txt):
    """
    Cleans and standardizes text by converting it to lowercase and handling missing values.

    Args:
        txt (str): Input text to clean.

    Returns:
        str: Lowercase cleaned text, or an empty string if the input is NaN.
    """
    if pd.isna(txt):
        return ""
    return txt.lower()

# Initialize parsedatetime Calendar
cal = parsedatetime.Calendar()

# Function for initial note type screening
def initial_screening(note_type):
    """
    Performs an initial check on the note type to determine if further processing is needed.

    Args:
        note_type (str): The type of the note (e.g., 'Triage note', 'H&P').

    Returns:
        bool: True if the note type is valid for processing, False otherwise.
    """
    valid_note_types = ['Triage note', 'H&P', 'ED Screening - First Contact']
    return note_type in valid_note_types

# Method 1: Simple fallback parsing
def process_with_method_1(val, note_date):
    """
    Processes text for datetime expressions using the parsedatetime library.

    Args:
        val (str): Text to process for date and time expressions.
        note_date (datetime): Reference datetime to resolve relative dates.

    Returns:
        list: A list of tuples containing detected times and their corresponding expressions.
    """
    date_res = cal.nlp(val, note_date)
    detected_times = []

    for tup in date_res or []:
        if tup[0].year != note_date.year:
            continue
        detected_time = tup[0].strftime("%m/%d/%Y %H:%M:%S")
        detected_times.append((detected_time, tup[4]))
    return detected_times

# Method 2: Advanced parsing
def process_with_method_2(clean_notes, note_datetime):
    """
    Advanced method to process text for datetime expressions and contextual relevance.

    Args:
        clean_notes (str): Cleaned note text to analyze.
        note_datetime (str): The note datetime string in "%Y-%m-%d %H:%M:%S" format.

    Returns:
        dict: A dictionary with detected times and all parsed times.
            - "time_detected_list": Times with contextual relevance (e.g., mentioning "pain").
            - "all_detected_times": All detected date and time expressions in the text.
    """
    note_date = datetime.strptime(note_datetime, "%Y-%m-%d %H:%M:%S")

    # Split text into sentences with their indices
    sentences = clean_notes.split(".")
    sentences_with_idx = [(sentence, clean_notes.index(sentence)) for sentence in sentences]

    # Parse datetime expressions
    date_res = cal.nlp(clean_notes, note_date)
    time_detected_list = []
    all_detected_times = []

    for tup in date_res or []:
        parsed_time = tup[0]
        time_expression = tup[4]

        # Check for explicit numeric times (e.g., "2:30 PM")
        explicit_time_match = re.search(r'(\d{1,2}[:.]\d{2}\s*(am|pm)?)', time_expression, re.IGNORECASE)
        if explicit_time_match:
            explicit_time_str = explicit_time_match.group(1).replace(".", ":").strip()
            explicit_time_str = re.sub(r'(?<=\d)(am|pm)$', r' \1', explicit_time_str, flags=re.IGNORECASE)

            try:
                # Handle missing AM/PM or 24-hour format
                if not re.search(r'(am|pm)', explicit_time_str, re.IGNORECASE):
                    explicit_time = datetime.strptime(explicit_time_str, "%H:%M").time()
                else:
                    explicit_time = datetime.strptime(explicit_time_str, "%I:%M %p").time()

                parsed_time = datetime.combine(parsed_time.date(), explicit_time)
            except ValueError as e:
                print(f"Skipping invalid time format: '{explicit_time_str}' - {e}")

        # Add detected times and expressions to the list
        detected_time = parsed_time.strftime("%m/%d/%Y %H:%M:%S")
        all_detected_times.append((detected_time, time_expression))

        # Check for sentences containing the word "pain"
        for sentence, idx in sentences_with_idx:
            if tup[2] < idx:
                break
            if "pain" in sentence:
                time_detected_list.append((detected_time, time_expression))

    if not time_detected_list:
        time_detected_list = all_detected_times

    return {
        "time_detected_list": time_detected_list,
        "all_detected_times": all_detected_times
    }

# Combined method
def process_single_note(note_type, clean_notes, note_datetime):
    """
    Combines an initial screening, advanced parsing (Method 2), and fallback parsing (Method 1).

    Args:
        note_type (str): Type of the note to check for validity.
        clean_notes (str): Cleaned note text to analyze.
        note_datetime (str): The note datetime string in "%Y-%m-%d %H:%M:%S" format.

    Returns:
        list: A list of detected times and their corresponding expressions, or an empty list if the note type is invalid.
    """
    # Initial screening
    if not initial_screening(note_type):
        print(f"Skipping processing for note type: {note_type}")
        return []

    note_date = datetime.strptime(note_datetime, "%Y-%m-%d %H:%M:%S")

    # Process using Method 2
    method_2_result = process_with_method_2(clean_notes, note_datetime)

    if not method_2_result["time_detected_list"]:
        # Fallback to Method 1A
        return process_with_method_1(clean_notes, note_date)

    return method_2_result["time_detected_list"]

# Example usage
if __name__ == "__main__":
    # Example input
    example_note_type = "Triage note"A
    example_clean_notes = "c/o midsternal chest pain radiating to right arm and neck since 0530 today."
    example_note_datetime = "2018-01-12 13:12:00"

    # Process the single note
    detected_times = process_single_note(example_note_type, example_clean_notes, example_note_datetime)

    # Output the results
    print("Detected Times:", detected_times)
