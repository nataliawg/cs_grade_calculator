from grade_calculator.models import Evaluation
from grade_calculator.calculator import GradeCalculator


def run():
    print(">>> CS-GradeCalculator demo <<<")

    evaluations = [
        Evaluation("Parcial 1", 15.0, 30.0),
        Evaluation("Parcial 2", 18.0, 30.0),
        Evaluation("Proyecto", 17.0, 40.0),
    ]

    attendance = 85.0
    extra_policy_enabled = True

    calculator = GradeCalculator()
    breakdown = calculator.calculate_final_grade(
        evaluations=evaluations,
        attendance_percentage=attendance,
        extra_policy_enabled=extra_policy_enabled,
    )

    print(f"Promedio ponderado: {breakdown.weighted_average:.2f}")
    print(f"Penalización asistencia: {breakdown.attendance_penalty:.2f}")
    print(f"Puntos extra: {breakdown.extra_points:.2f}")
    print(f"Nota final: {breakdown.final_grade:.2f}")


if __name__ == "__main__":
    run()
