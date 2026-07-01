import re


def clean_text(text):

    if not text:
        return ""

    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def normalize_name(name):

    return clean_text(
        name
    ).lower()