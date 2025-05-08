# WebScraping do site do Livro dos recordes!

Essa captura de dados foi realiza com o framework **Playwright** seguindo os princípios da arquitetura limpa com exportação dos dados para CSV e logs de erros.

## Arquitetura
|                 |                           						|
|-----------------|-------------------------------------------------|
|/main			  |`Arquivo inicial`              				   	|
|/model           |`Entidades do sistema`          				   	|
|/controller      |`Caso de uso do sistema`            			   	|
|/service         |`Funções de auxilio para o controlador`          |
|/utils           |`Utilitários e funções de auxilio para o serviço`|


## Instalação

- Criar o ambiente virtual `python -m venv venv`
- Instalar as dependências `pip install -r requirements.txt`

## Execução

- ``` python main.py get_all ```
Execute a captura de todos os recordes.

- ``` python main.py get_by_category --category animais ```
Execute a captura dos recordes que tem a categoria "animais".

- ``` python main.py get_by_title --title veneno ```
Execute a captura dos recordes que tem o titulo "veneno".
