import argparse
from src.controller.controller_records import get_records_by_category

def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", help="Comandos disponiveis")

    # parametro --get_by_category
    cmd_get_by_category = commands.add_parser("get_by_category", help="Obter records por categoria")
    cmd_get_by_category.add_argument("--category", required=True, help="Categoria dos records")
    cmd_get_by_category.set_defaults(func=get_records_by_category)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()