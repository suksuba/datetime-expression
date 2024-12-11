import re

# Define time-related regex patterns
patterns = {
    "pattern1": re.compile(
        r"(([01]?[0-9]|2[0-3])(:[0-5][0-9])?\s*([aApP][mM]))\s*(((this|next|last)?\s*(morning|afternoon|noon|night|tonight|evening|today|yesterday)))?",
        re.IGNORECASE,
    ),
    "pattern2": re.compile(
        r"((0[0-9][0-5][0-9]|[1-9][0-5][0-9][0-9]))\s*(((this|next|last)?\s*(morning|afternoon|noon|night|tonight|evening|today|yesterday)))?",
        re.IGNORECASE,
    ),
    "pattern3": re.compile(
        r"(([01]?[0-9]|2[0-3])(:[0-5][0-9])?\s*([aApP][mM])?)\s*(morning|afternoon|noon|night|evening)",
        re.IGNORECASE,
    ),
    "pattern4": re.compile(
        r"(((this|next|last)?\s*(morning|afternoon|noon|night|tonight|evening|today|yesterday)))\s*(([01]?[0-9]|2[0-3])(:[0-5][0-9])?\s*([aApP][mM])?)",
        re.IGNORECASE,
    ),
    "pattern5": re.compile(
        r"(((this|next|last)?\s*(morning|afternoon|noon|night|tonight|evening|today|yesterday)))\s*(((0[0-9][0-5][0-9]|[1-9][0-5][0-9][0-9]))|(([01]?[0-9]|2[0-3])(:[0-5][0-9])?\s*([aApP][mM])?))",
        re.IGNORECASE,
    ),
    "pattern_iso": re.compile(
        r"((^|(?<=\s))(1|2|3|4|5|6|7|8|9|10|11|12|01|02|03|04|05|06|07|08|09)[/.]\d{1,2}[/.]\d{2,4}(?=\D))",
        re.IGNORECASE,
    ),
    "pattern7": re.compile(
        r"(([01]?[0-9]|2[0-3]):[0-5][0-9]\s*([aApP][mM])?)\s*yesterday", re.IGNORECASE
    ),
    "pattern8": re.compile(
        r"(([01]?[0-9]|2[0-3]):[0-5][0-9]\s*([aApP][mM])?)\s*today", re.IGNORECASE
    ),
}

def clean_text(text):
    """
    Clean text by converting to lowercase and stripping extra whitespace.
    Args:
        text (str): Input text to clean.
    Returns:
        str: Cleaned and normalized text.
    """
    return str(text).lower().strip() if text else ""

def match_pattern(pattern, text):
    """
    Matches all occurrences of a regex pattern in the input text.
    Args:
        pattern (re.Pattern): Compiled regex pattern to match.
        text (str): Input text to search within.
    Returns:
        list: List of all matched strings.
    """
    matches = []
    start_pos = 0
    while True:
        match = re.search(pattern, text[start_pos:])
        if match:
            matches.append(match.group(0))
            start_pos += match.end()  # Move start position to end of the last match
        else:
            break
    return matches

def process_single_input(text):
    """
    Process a single input text, matching multiple patterns and logging results.
    Args:
        text (str): The clinical note or sentence to process.
    Returns:
        dict: A dictionary containing matched patterns and their corresponding matches.
    """
    # Clean the input text
    cleaned_text = clean_text(text)
    results = {}

    print("Processing Input:")
    print(f"Text: {cleaned_text}")
    print()

    # Match all patterns and store results
    for pattern_name, pattern in patterns.items():
        matches = match_pattern(pattern, cleaned_text)
        results[pattern_name] = matches
        print(f"Pattern: {pattern_name}")
        if matches:
            for match in matches:
                print(f"Matched: {match}")
        else:
            print("No matches found.")
        print()

    return results

# Example usage
if __name__ == "__main__":
    # Example input
    example_text = "Patient reported experiencing pain at 10:30 PM yesterday and 8:00 AM today."

    # Process the example text
    process_single_input(example_text)
