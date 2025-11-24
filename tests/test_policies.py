import pytest

from grade_calculator.policies import AttendancePolicy, ExtraPointsPolicy


def test_attendance_policy_should_return_true_when_above_minimum():
    policy = AttendancePolicy(minimum_percentage=70.0)

    assert policy.has_minimum_attendance(80.0) is True
    assert policy.has_minimum_attendance(70.0) is True


def test_attendance_policy_should_return_false_when_below_minimum():
    policy = AttendancePolicy(minimum_percentage=70.0)

    assert policy.has_minimum_attendance(60.0) is False


def test_attendance_policy_should_raise_error_when_attendance_out_of_range():
    policy = AttendancePolicy()

    with pytest.raises(ValueError):
        policy.has_minimum_attendance(-1.0)

    with pytest.raises(ValueError):
        policy.has_minimum_attendance(150.0)


def test_attendance_policy_should_zero_grade_when_attendance_is_insufficient():
    policy = AttendancePolicy(minimum_percentage=75.0)
    # base grade 18, pero asistencia 50% < 75% => nota pasa a 0
    result = policy.apply_penalty(base_grade=18.0, attendance_percentage=50.0)
    assert result == 0.0


def test_attendance_policy_should_keep_grade_when_attendance_is_sufficient():
    policy = AttendancePolicy(minimum_percentage=75.0)
    result = policy.apply_penalty(base_grade=18.0, attendance_percentage=80.0)
    assert result == 18.0


def test_extra_points_policy_should_return_zero_when_disabled():
    policy = ExtraPointsPolicy(max_extra_points=2.0, threshold_for_extra=15.0)

    extra = policy.calculate_extra_points(base_grade=18.0, extra_policy_enabled=False)
    assert extra == 0.0


def test_extra_points_policy_should_add_points_when_enabled_and_grade_above_threshold():
    policy = ExtraPointsPolicy(max_extra_points=2.0, threshold_for_extra=15.0)

    extra = policy.calculate_extra_points(base_grade=18.0, extra_policy_enabled=True)
    assert extra == 1.0   # con la regla que pusimos: +1 punto


def test_extra_points_policy_should_not_add_points_when_grade_below_threshold():
    policy = ExtraPointsPolicy(max_extra_points=2.0, threshold_for_extra=15.0)

    extra = policy.calculate_extra_points(base_grade=14.9, extra_policy_enabled=True)
    assert extra == 0.0
