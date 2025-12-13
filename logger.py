import logging
import json
from datetime import datetime

def get_logger(component_name):
    logger = logging.getLogger(component_name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()

        def format(record):
            log = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "component": component_name,
                "message": record.getMessage()
            }
            if hasattr(record, "error_code"):
                log["error_code"] = record.error_code
            return json.dumps(log)

        handler.setFormatter(logging.Formatter(fmt="%(message)s"))
        logger.addHandler(handler)
        logger.format = format

    return logger
