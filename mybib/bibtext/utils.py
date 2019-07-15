import re


def _split_by(text, separator=",|;"):
    return [i.strip() for i in re.split(separator, text.replace("\n", ""))]
