from dataclasses import dataclass

@dataclass
class ContractContent:
    passage: str
    filename: str
    confidence: float
    pagenumber: int

@dataclass
class ContractSummary:
    passage: str
    filename: str
    confidence: float
