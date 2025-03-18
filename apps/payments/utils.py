import hashlib
import os
from venv import logger
from django.conf import settings

from config.settings import CLICK_SERVICE_ID, CLICK_MERCHANT_ID


CLICK_SECRET_KEY = os.environ.get('CLICK_SECRET_KEY'),


from click_up import ClickUp


click_up = ClickUp(service_id=f"{CLICK_SERVICE_ID}", merchant_id=f"{CLICK_MERCHANT_ID}")


paylink = click_up.initializer.generate_pay_link(
  id=4, 
  amount=1000,
  return_url="https://example.com"
)

