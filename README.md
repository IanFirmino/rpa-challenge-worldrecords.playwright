# WebScraping do site do Livro dos recordes!

Essa captura de dados foi realiza com o framework **Playwright** seguindo os princípios da arquitetura limpa com exportação dos dados para CSV e caso necessário logs de erros.

A extração dos dados é do site https://www.guinnessworldrecords.com.br/records/showcase
e é capturado as principais informações por Record.

## Arquitetura
|                 |                           						|
|-----------------|-------------------------------------------------|
|/main			  |`Arquivo principal para execução dos comandos via terminal`              				   	|
|/model           |`Entidades e modelos da aplicação`          				   	|
|/controller      |`Casos de uso que coordenam a lógica da aplicação`            			   	|
|/service         |`Funções responsáveis por interações e extração dos dados`          |
|/utils           |`Funções auxiliares (log, formatação, helpers, etc.)`|


## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/IanFirmino/rpa-challenge-worldrecords.webscraping.git
   cd projeto
   ```

2. Crie o ambiente virtual:
   ```
   python -m venv venv
   ```

3. Ative o ambiente:
     ```
     venv\Scripts\activate
     ```


4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```


- Criar o ambiente virtual `python -m venv venv`
- Instalar as dependências `pip install -r requirements.txt`


## Execução

Utilize o `main.py` com o comando abaixo para realizar a captura dos dados:

### Filtrar por categoria:
```
python -m src.main get_by_category --category "Maratonas"
python -m src.main get_by_category --category "Aprendendo"
python -m src.main get_by_category --category "Moda e maquiagem"
```

## Exportações

Todos os resultados extraídos são salvos automaticamente na pasta `/exportations` com o nome da categoria/título e a data/hora da execução.
Eventuais erros também são gerados na `/exportations`.
