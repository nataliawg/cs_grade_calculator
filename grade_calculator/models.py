from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Evaluation:
    name: str
    score: float       
    weight: float     

@dataclass(frozen=True)
class GradeBreakdown:
    weighted_average: float
    attendance_penalty: float
    extra_points: float
    final_grade: float
