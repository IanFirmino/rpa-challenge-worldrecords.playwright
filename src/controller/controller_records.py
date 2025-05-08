from src.service.records import find_all_records, export_csv

def get_all_records():
    try:
        records = find_all_records()
        export_csv(records)
    except Exception as ex:
        print(ex)
        return ex #gerar log do error