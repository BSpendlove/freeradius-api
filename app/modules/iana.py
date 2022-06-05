from ttp import ttp
import requests
from typing import List
from loguru import logger

from app.config.app import get_settings
from app.schemas_old import IANAPrivateEnterprise


def get_iana_numbers() -> List[IANAPrivateEnterprise]:
    settings = get_settings()
    iana_enterprise_numbers = requests.get(settings.iana_enterprise_numbers)

    if not iana_enterprise_numbers:
        logger.error("Unable to gather IANA Enterprise Numbers")
        return

    response_text = iana_enterprise_numbers.text
    headers = """Decimal
| Organization
| | Contact
| | | Email
| | | |"""
    start = response_text.find(headers) + len(headers)
    ttp_template = """{{ iana_number | DIGIT }}
  {{ organization | ROW | WORD }}
    """

    parser = ttp(data=response_text[start : len(response_text)], template=ttp_template)
    parser.parse()

    results = parser.result()[0]
    if not results:
        return
    return results[0]
