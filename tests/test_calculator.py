import pytest
from grade_calculator.models import Evaluation
from grade_calculator.calculator import GradeCalculator
from grade_calculator.policies import AttendancePolicy


def test_should_return_weighted_average_when_normal_case():
    calculator = GradeCalculator()
    evaluations = [
        Evaluation("Eval1", 10.0, 50.0),
        Evaluation("Eval2", 20.0, 50.0),
    ]

    breakdown = calculator.calculate_final_grade(
        evaluations=evaluations,
        attendance_percentage=80.0,
        extra_policy_enabled=False,
    )

    assert breakdown.weighted_average == 15.0
    assert breakdown.final_grade == pytest.approx(15.0)


def test_should_return_zero_when_attendance_below_minimum():
    calculator = GradeCalculator()
    evaluations = [
        Evaluation("Eval1", 18.0, 100.0),
    ]

    breakdown = calculator.calculate_final_grade(
        evaluations=evaluations,
        attendance_percentage=50.0,  # por debajo del 70%
        extra_policy_enabled=True,
    )

    assert breakdown.weighted_average == 18.0
    assert breakdown.final_grade == 0.0  # penalización total


def test_should_add_extra_points_when_policy_enabled_and_grade_high():
    calculator = GradeCalculator()
    evaluations = [
        Evaluation("Eval1", 18.0, 100.0),
    ]

    breakdown = calculator.calculate_final_grade(
        evaluations=evaluations,
        attendance_percentage=100.0,
        extra_policy_enabled=True,
    )

    assert breakdown.weighted_average == 18.0
    assert breakdown.extra_points == pytest.approx(1.0)
    assert breakdown.final_grade == pytest.approx(19.0)


def test_should_not_add_extra_points_when_policy_disabled():
    calculator = GradeCalculator()
    evaluations = [
        Evaluation("Eval1", 18.0, 100.0),
    ]

    breakdown = calculator.calculate_final_grade(
        evaluations=evaluations,
        attendance_percentage=100.0,
        extra_policy_enabled=False,
    )

    assert breakdown.extra_points == 0.0
    assert breakdown.final_grade == pytest.approx(18.0)


def test_should_handle_zero_evaluations_without_error():
    calculator = GradeCalculator()
    breakdown = calculator.calculate_final_grade(
        evaluations=[],
        attendance_percentage=100.0,
        extra_policy_enabled=True,
    )

    assert breakdown.weighted_average == 0.0
    assert breakdown.final_grade == 0.0


def test_should_raise_error_when_weights_do_not_add_up_to_100():
    calculator = GradeCalculator()
    evaluations = [
        Evaluation("Eval1", 10.0, 40.0),
        Evaluation("Eval2", 10.0, 40.0),
    ]

    with pytest.raises(ValueError):
        calculator.calculate_final_grade(
            evaluations=evaluations,
            attendance_percentage=100.0,
            extra_policy_enabled=False,
        )


def test_should_raise_error_when_attendance_negative():
    calculator = GradeCalculator()
    evaluations = [
        Evaluation("Eval1", 15.0, 100.0),
    ]

    with pytest.raises(ValueError):
        calculator.calculate_final_grade(
            evaluations=evaluations,
            attendance_percentage=-10.0,
            extra_policy_enabled=False,
        )
