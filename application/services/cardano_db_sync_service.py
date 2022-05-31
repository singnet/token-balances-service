from common.logger import get_logger
from config import CARDANO_DB_SYNC_SERVICE_API_BASE_PATH, CARDANO_DB_SYNC_SERVICE_API_KEY
from constants.status import ApiMethodType
from utils.api import call_api

logger = get_logger(__name__)


class CardanoDBSyncService:

    def __init__(self):
        pass

    @staticmethod
    def get_asset_holders(policy_id, asset_name):
        logger.info(f"Getting the asset holders for the policy_id={policy_id}, asset_name={asset_name}")
        return call_api(url=CARDANO_DB_SYNC_SERVICE_API_BASE_PATH,
                        headers={"Content-Type": "application/json", "X-API-Key": CARDANO_DB_SYNC_SERVICE_API_KEY},
                        method_type=ApiMethodType.GET.value)
