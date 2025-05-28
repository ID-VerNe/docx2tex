# --- ADD: Module docstring ---
"""Configuration loading utility."""
# --- END ADD ---
import os
import logging
from dotenv import load_dotenv

# --- ADD: Configure basic logging ---
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s.%(funcName)s] - %(message)s')
logger = logging.getLogger(__name__)
# --- END ADD ---

# --- ADD: Load environment variables from .env file ---
load_dotenv()
logger.info("Loaded environment variables from .env file.")
# --- END ADD ---

def get_config(key, default=None):
    # --- ADD: Function docstring ---
    """
    Retrieves a configuration value from environment variables.

    Args:
        key: The name of the environment variable.
        default: The default value if the variable is not set.

    Returns:
        The retrieved configuration value or the default value.
    """
    # --- END ADD ---
    logger.debug(f"Attempting to get config key: {key}")
    value = os.getenv(key, default)
    if value is not None:
        logger.debug(f"Config key '{key}' retrieved successfully.")
    else:
        logger.warning(f"Config key '{key}' not found, using default value: {default}")
    return value

if __name__ == "__main__":
    logger.info("Testing config loading...")
    test_value = get_config("TEST_KEY", "default_test_value")
    print(f"TEST_KEY value: {test_value}")
    non_existent_value = get_config("NON_EXISTENT_KEY")
    print(f"NON_EXISTENT_KEY value: {non_existent_value}")
    logger.info("Config loading test finished.")