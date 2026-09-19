from dataclasses import dataclass

import numpy as np


@dataclass
class Detection:
    metric: str
    current_value: float
    moving_average: float
    standard_deviation: float
    severity: str
    description: str


def detect_error_spike(error_count: int, history: list[int], sigma: float = 2.0) -> Detection | None:
    values = np.asarray(history, dtype=float)
    if len(values) < 2:
        return None
    moving_average = float(values.mean())
    standard_deviation = float(values.std())
    limit = moving_average + sigma * standard_deviation
    if error_count <= limit or error_count <= moving_average:
        return None
    severity = "critical" if error_count >= max(10, limit * 1.5) else "warning"
    return Detection("error_count", float(error_count), moving_average, standard_deviation, severity, f"Error count {error_count} exceeded the moving-average limit of {limit:.2f}.")