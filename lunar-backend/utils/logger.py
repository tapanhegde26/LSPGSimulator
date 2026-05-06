import logging

# Create logger
logger = logging.getLogger("lunar_simulator")

# Set level
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

# Add handler (avoid duplicate handlers)
if not logger.handlers:
    logger.addHandler(console_handler)