"""Pepperoni testing."""

import pepperoni


logger = pepperoni.logger()
text = 'Very interesting information'
logger.info(text)
logger.debug(text)
logger.error(text)
logger.warning(text)
logger.critical(text)
