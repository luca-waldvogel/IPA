from jobfit.app import lambda_handler

from .app_context import AppContext
from .main import handle


@lambda_handler(lambda: AppContext())
def handler(event, context):
    return handle(event)
