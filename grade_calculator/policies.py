from dataclasses import dataclass
from typing import List
from .models import Evaluation


@dataclass(frozen=True)
class AttendancePolicy:
    minimum_percentage: float = 70.0

    def has_minimum_attendance(self, attendance_percentage: float) -> bool:
        if attendance_percentage < 0 or attendance_percentage > 100:
            raise ValueError("Attendance percentage must be between 0 and 100.")
        return attendance_percentage >= self.minimum_percentage

    def apply_penalty(self, base_grade: float, attendance_percentage: float) -> float:
        
       
        if not self.has_minimum_attendance(attendance_percentage):
            return 0.0
        return base_grade


@dataclass(frozen=True)
class ExtraPointsPolicy:


    max_extra_points: float = 2.0
    threshold_for_extra: float = 15.0

    def calculate_extra_points(
        self,
        base_grade: float,
        extra_policy_enabled: bool
    ) -> float:
      
        if not extra_policy_enabled:
            return 0.0

        if base_grade >= self.threshold_for_extra:
            return min(1.0, self.max_extra_points)
        return 0.0
