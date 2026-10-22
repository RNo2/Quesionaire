"""Construct a bounded answer plan, then render it; no random quote shuffling."""

from dataclasses import dataclass
from hashlib import sha256


def select(bank, question, component):
    # Python's built-in hash changes between processes; SHA-256 does not.
    number = int.from_bytes(sha256(f"{question}|{component}".encode()).digest()[:8], "big")
    return bank[number % len(bank)]


@dataclass(frozen=True)
class AnswerPlan:
    position: str
    reasoning: tuple[str, ...]
    distinction: str
    implication: str
    closing: str = ""
    qualification: str = ""

    def render(self):
        # Suppress exact repetition across components while retaining argument
        # order: position -> grounds -> consequence -> distinction -> limit.
        seen = set()

        def fresh(parts):
            result = []
            for part in parts:
                if part and part not in seen:
                    seen.add(part)
                    result.append(part)
            return " ".join(result)

        paragraphs = (
            fresh((self.position,)),
            fresh(self.reasoning),
            fresh((self.implication, self.closing)),
            fresh((self.distinction,)),
            fresh((self.qualification,)),
        )
        return "\n\n".join(part for part in paragraphs if part)
