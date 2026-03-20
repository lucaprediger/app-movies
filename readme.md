# Desafio API - Golden Raspberry Awards

Esta API RESTful foi desenvolvida para possibilitar a leitura da lista de indicados e vencedores da categoria **"Pior Filme"** do **Golden Raspberry Awards** a partir de um arquivo CSV e calcular os intervalos entre prêmios de produtores.

---

## 1. Instalação das Dependências

Certifique-se de ter o **Python 3.11+** instalado.

Para instalar todas as bibliotecas necessárias, execute o comando abaixo na raiz do projeto:

pip install -r requirements.txt

---

## 2. Executando a API com Uvicorn

Para subir o servidor e carregar os dados do CSV automaticamente para o banco de dados em memória.

### Modo padrão (sem logs de debug)

uvicorn main:app

### Modo com logs habilitados

Para visualizar as mensagens do logger sobre a leitura do CSV e a persistência no banco:

uvicorn main:app --log-level debug

---

## 3. Testes de Integração

Para rodar todos os testes:

pytest

Para rodar um arquivo específico:

pytest tests/test_movies.py

---

## 4. Como consumir a API

A API estará disponível por padrão em:

[http://localhost:8000](http://localhost:8000)

### Consultar Intervalos de Prêmios

Retorna:

* o produtor com **maior intervalo** entre dois prêmios consecutivos
* o produtor com **menor intervalo** entre dois prêmios consecutivos

### Chamada via cURL

curl -X GET "[http://localhost:8000/awards/get-awards-interval](http://localhost:8000/awards/get-awards-interval)" -H "accept: application/json"

---

## 5. Detalhes Técnicos

**Banco de Dados**

* SQLite em memória (`:memory:`)
* Utilizando `StaticPool`

**ORM**

* SQLModel (SQLAlchemy + Pydantic)

**Carga de Dados**

* O arquivo CSV é processado automaticamente no evento de inicialização (`lifespan`) da aplicação.

---

## 6. Atenção

Para que o sistema de importação funcione corretamente (especialmente a lógica de separar nomes por vírgula ou pelo termo `"and"`), o padrão das colunas **producers** e **studios** deve ser seguido à risca, conforme o CSV disponibilizado.

Adicionar ao **item 7 do README** a estrutura de pastas conforme a imagem:

## 7. Estrutura do Projeto

```
app-movies/
│
├── controller/
│   └── award.py
│
├── csv/
│   └── movielist.csv
│
├── database/
│   └── database.py
│
├── models/
│   ├── database/
│   │   └── movie.py
│   │
│   └── response/
│       └── award_response.py
│
├── service/
│   └── movies.py
│
├── tests/
│   ├── conftest.py
│   └── test_movies.py
│
├── utils/
│   └── logging.py
│
├── main.py
├── requirements.txt
└── README.md
```

Descrição resumida:

* **controller/** – endpoints da API
* **csv/** – arquivos CSV utilizados para carga de dados
* **database/** – configuração e criação do banco
* **models/** – modelos ORM e modelos de resposta da API
* **service/** – regras de negócio
* **tests/** – testes de integração com pytest
* **utils/** – utilidades gerais (ex.: logging)
* **main.py** – inicialização da aplicação FastAPI.
