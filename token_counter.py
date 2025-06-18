import re

class SimpleTokenCounter:
    def __init__(self):
        self.word_pattern = re.compile(r"\w+|\S")
        
    def count_tokens(self, text):
        """Approximate token counting by splitting words and punctuation"""
        return len(self.word_pattern.findall(text)) if text else 0