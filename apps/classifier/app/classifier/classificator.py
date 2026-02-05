from .rules import CLASSIFICATION_RULES
import re

class TransactionClassificator:

    def __init__(self):
        self._compile_rules_patterns()

    def _compile_rules_patterns(self):
        self.compiled_rules = {}
        for category, patterns in CLASSIFICATION_RULES.items():
            self.compiled_rules[category] = [re.compile(
                rf"\b{re.escape(pattern)}\b", re.IGNORECASE) for pattern in patterns]
            
    def _match_category(self, transaction_description: str) -> str:
        matches = []

        for category, patterns in self.compiled_rules.items():
            match_count = 0

            for pattern in patterns: 
                if pattern.search(transaction_description):
                    match_count += 1
                    break

            if match_count > 0:
                matches.append((category, match_count))
        
        return matches
    
    def classify(self, transaction_description: str) -> str:
        matches = self._match_category(transaction_description)

        if not matches:
            return "uncategorized"

        matches.sort(key=lambda x: x[1], reverse=True) # Order by match count descending

        return matches[0][0]  # Return the category with the highest match count