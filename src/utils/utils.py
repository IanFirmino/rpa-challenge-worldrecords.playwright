import os
import csv
import sys
import logging
from datetime import datetime
from fake_useragent import UserAgent
from logging.handlers import RotatingFileHandler

def get_proxy():
    proxies = [
        "http://127.0.0.1:8080"
    ]
    return proxies[0]

def get_user_agent():
    ua = UserAgent()
    return ua.chrome

def create_logger(log_name: str):
    try:
        save_dir = os.path.join(os.getcwd(), "exportations")
        os.makedirs(save_dir, exist_ok=True)
        log_file = os.path.join(save_dir, f'{log_name}.log')

        rotating_handler = RotatingFileHandler(
            filename=log_file, mode='a', maxBytes=5 * 1024 * 1024, backupCount=0, encoding='utf-8'
        )

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[logging.StreamHandler(), rotating_handler]
        )
    except:
        save_dir = os.path.dirname(sys.executable)
        log_file = os.path.join(save_dir, f'{log_name}.log')

        rotating_handler = RotatingFileHandler(
            filename=log_file, mode='a', maxBytes=5 * 1024 * 1024, encoding='utf-8'
        )

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[logging.StreamHandler(), rotating_handler]
        )

def export_csv(obj_list, title):
    save_dir = os.path.join(os.getcwd(), "exportations")
    os.makedirs(save_dir, exist_ok=True)

    fieldnames = set()
    for obj in obj_list:
        fieldnames.update(obj.__dict__.keys())
    fieldnames = list(fieldnames)

    filename = f'{title.upper()} - {datetime.now().strftime("%y%m%d%H%M%S")}.csv'
    filepath = os.path.join(save_dir, filename)

    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for obj in obj_list:
            row = {key: None for key in fieldnames}
            row.update(obj.__dict__)
            writer.writerow(row)
    return filepath