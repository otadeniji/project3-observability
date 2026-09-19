import re
from datetime import datetime, timezone

LOG_PATTERN = re.compile(r"^\[(?P<timestamp>[^]]+)\]\s+(?P<level>\w+):\s+(?P<message>.*)$")
NUMBER_PATTERN = re.compile(r"(?P<value>\d+(?:\.\d+)?)%")


def parse_line(line: str) -> dict | None:
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    timestamp = datetime.strptime(match.group("timestamp"), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    message = match.group("message")
    numeric_match = NUMBER_PATTERN.search(message)
    return {"timestamp": timestamp, "level": match.group("level").upper(), "message": message, "metric_value": float(numeric_match.group("value")) if numeric_match else None}


def parse_content(content: str) -> list[dict]:
    return [parsed for line in content.splitlines() if (parsed := parse_line(line))]