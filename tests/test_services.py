from app.services.anomaly_detector import detect_error_spike
from app.services.parser import parse_line


def test_parser_reads_sample_log_shape() -> None:
    parsed = parse_line("[2026-09-18 16:47:30] WARNING: High memory usage detected - 85%")
    assert parsed is not None
    assert parsed["level"] == "WARNING"
    assert parsed["metric_value"] == 85.0


def test_detector_flags_error_spike() -> None:
    detection = detect_error_spike(12, [0, 1, 0, 1, 0])
    assert detection is not None
    assert detection.severity == "critical"
    assert detection.metric == "error_count"


def test_detector_ignores_normal_value() -> None:
    assert detect_error_spike(1, [0, 1, 0, 1, 0]) is None


def test_detector_uses_history_as_baseline() -> None:
    detection = detect_error_spike(10, [3, 3])
    assert detection is not None
    assert detection.moving_average == 3.0