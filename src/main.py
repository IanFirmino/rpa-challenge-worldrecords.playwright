import argparse
from src.controller.controller_records import get_all_records, get_records_by_title, get_records_by_category

def main():
    parser = argparse.ArgumentParser(description="Script para manipulação de registros")
    subparsers = parser.add_subparsers(dest="command", help="Subcomandos disponíveis")

    # parametro --get_all
    subparser_get_all = subparsers.add_parser("get_all", help="Obter todos os registros")
    subparser_get_all.set_defaults(func=get_all_records)

    # parametro --get_by_category
    subparser_get_by_category = subparsers.add_parser("get_by_category", help="Obter registros por categoria")
    subparser_get_by_category.add_argument("--category", required=True, help="Categoria dos registros")
    subparser_get_by_category.set_defaults(func=get_records_by_category)

    # parametro --get_by_title
    subparser_get_by_title = subparsers.add_parser("get_by_title", help="Obter registros por título")
    subparser_get_by_title.add_argument("--title", required=True, help="Título dos registros")
    subparser_get_by_title.set_defaults(func=get_records_by_title)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()