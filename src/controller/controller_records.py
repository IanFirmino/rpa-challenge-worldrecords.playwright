from src.service.service_records import find_all_records, find_records_by_record_title, find_records_by_record_category
from src.utils.utils import *

def get_all_records():
    try:
        create_logger(log_name="GWR_GetAllRecords")
        records = find_all_records()
        export_csv(records)
    except Exception as ex:
        logging.info(msg=ex)

def get_records_by_title(title):
    try:
        create_logger(log_name="GWR_GetRecordsByTitle")
        records = find_records_by_record_title(title)
        export_csv(records)
    except Exception as ex:
        logging.info(msg=ex)

def get_records_by_category(category):
    try:
        create_logger(log_name="GWR_GetRecordsByCategory")
        records = find_records_by_record_category(category)
        export_csv(records)
    except Exception as ex:
        logging.info(msg=ex)