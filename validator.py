import re

bad_words = ["shit", "fuck","fucking","fucked", "damn", "crap", "bitch"]
allowed_punctuations = {".", ","}

def sanitize_input(text):
    """Clean up user input by removing extra spaces and weird characters."""
    sanitized = re.sub(r'\s+', ' ', text)
    sanitized = sanitized.strip()
    return sanitized

def validate_user_input_with_details(text):
    """Validate the user input and return (is_valid, message)."""
    text = sanitize_input(text)

    if not text:
        return False, "Input is empty."
    
    text_no_space = text.strip()
    if not text_no_space:
        return False, "Input contains only spaces."

    text_without_punctuations = ''.join(char for char in text_no_space if char.isalnum())
    if not text_without_punctuations:
        return False, "Input contains only punctuations or symbols."

    # Check for bad words
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    for word in words:
        if word in bad_words:
            return False, f"Input contains the word: '{word}', its not allowed."

    # Check for disallowed characters
    disallowed_chars = set()
    for char in text:
        if not (char.isalnum() or char.isspace() or char in allowed_punctuations):
            disallowed_chars.add(char)
    
    if disallowed_chars:
        disallowed_list = ', '.join(f"**{char}**" for char in sorted(disallowed_chars))
        return False, f"Input contains disallowed characters: {disallowed_list}.\nAllowed punctuations are only: {', '.join(sorted(allowed_punctuations))}"

    return True, "Input is valid."