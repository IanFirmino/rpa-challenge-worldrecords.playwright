import traceback
from src.service.service_records import find_records_by_category
from src.utils.utils import *

def get_records_by_category(args):
    try:
        category = args.category
        create_logger(log_name="GWR_GetRecordsByCategory")
        records = find_records_by_category(category)
        export_csv(records, category)
    except Exception as ex:
        err = traceback.format_exc()
        logging.info(msg=err)