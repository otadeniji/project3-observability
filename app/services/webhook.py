import logging

logger = logging.getLogger(__name__)


def simulate_webhook(alert_payload: dict) -> str:
    logger.info("Simulated webhook delivery: %s", alert_payload)
    return "simulated"