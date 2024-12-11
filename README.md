# Clinical Note Datetime Extraction

This repository contains two Python scripts for extracting and processing datetime expressions from clinical notes. Both scripts are optimized for single input processing and utilize `parsedatetime` and regular expressions.

---

## Scripts Overview

### 1. `parsedatetime.py`
Processes a single clinical note using `parsedatetime` to extract datetime expressions.

#### Key Features:
- Matches datetime expressions like `0530 today` or `10:30 PM yesterday`.
- Associates detected expressions with sentences containing them.
- Filters results based on the note's year.

#### Example:
Input:
```python
sentence = "c/o midsternal chest pain radiating to right arm and neck since 0530 today."
phrase = "0530 today"
note_date = "2018-01-12 13:12:00"
```

Output:
```plaintext
Sentence: c/o midsternal chest pain radiating to right arm and neck since 0530 today
Phrase: 0530 today
Time Detected: 01/12/2018 05:30:00
```

---

### 2. `REGEX.py`
Uses multiple regular expressions to extract datetime-related patterns from a clinical note.

#### Key Features:
- Matches formats like `10:30 PM yesterday`, `0530`, and `1/12/2018`.
- Supports relative terms like `today`, `yesterday`, and `last night`.
- Prints matches for each pattern.

#### Example:
Input:
```python
text = "Patient reported experiencing pain at 10:30 PM yesterday and 8:00 AM today."
```

Output:
```plaintext
Processing Input:
Text: patient reported experiencing pain at 10:30 pm yesterday and 8:00 am today.

Pattern: pattern1
No matches found.

Pattern: pattern3
Matched: 10:30 PM
Matched: 8:00 AM

Pattern: pattern7
Matched: 10:30 PM yesterday

Pattern: pattern8
Matched: 8:00 AM today
```

---

## Requirements

- Python 3.x
- Libraries:
  - `re` (built-in)
  - `datetime` (built-in)
  - [`parsedatetime`](https://pypi.org/project/parsedatetime/)

Install dependencies:
```bash
pip install parsedatetime
```
