from typing import List
from .models import Evaluation, GradeBreakdown
from .policies import AttendancePolicy, ExtraPointsPolicy


class GradeCalculator:
 
    MAX_EVALUATIONS = 10

    def __init__(
        self,
        attendance_policy: AttendancePolicy | None = None,
        extra_points_policy: ExtraPointsPolicy | None = None,
    ) -> None:
        self._attendance_policy = attendance_policy or AttendancePolicy()
        self._extra_points_policy = extra_points_policy or ExtraPointsPolicy()

    def calculate_final_grade(
        self,
        evaluations: List[Evaluation],
        attendance_percentage: float,
        extra_policy_enabled: bool,
    ) -> GradeBreakdown:
        if len(evaluations) > self.MAX_EVALUATIONS:
            raise ValueError("A student cannot have more than 10 evaluations.")

        if len(evaluations) == 0:
            base_average = 0.0
        else:
            base_average = self._calculate_weighted_average(evaluations)

        after_attendance = self._attendance_policy.apply_penalty(
            base_average, attendance_percentage
        )

        extra_points = self._extra_points_policy.calculate_extra_points(
            after_attendance, extra_policy_enabled
        )

        final_grade = max(0.0, min(after_attendance + extra_points, 20.0))

        return GradeBreakdown(
            weighted_average=base_average,
            attendance_penalty=after_attendance - base_average,
            extra_points=extra_points,
            final_grade=final_grade,
        )

    def _calculate_weighted_average(self, evaluations: List[Evaluation]) -> float:
  
        total_weight = sum(eval.weight for eval in evaluations)
        if total_weight <= 0:
            raise ValueError("Total weight must be positive")
        if abs(total_weight - 100.0) > 1e-6:
            raise ValueError("Total weight of evaluations must be 100%.")

        for evaluation in evaluations:
            if evaluation.score < 0 or evaluation.score > 20:
                raise ValueError("Evaluation score must be between 0 and 20.")
            if evaluation.weight < 0:
                raise ValueError("Evaluation weight cannot be negative.")

        weighted_sum = sum(
            evaluation.score * (evaluation.weight / 100.0)
            for evaluation in evaluations
        )
        return weighted_sum
