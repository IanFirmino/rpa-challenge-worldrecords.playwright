from src.service.records import find_all_records, export_csv

def get_all_records():
    try:
        pokemons = find_all_records()
        export_csv(pokemons)
    except Exception as ex:
        return ex #gerar log do error