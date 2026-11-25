# API de Gerenciamento de Tarefas

API REST desenvolvida em Python com FastAPI e SQLite para gerenciamento de tarefas, utilizando uma arquitetura modular e separação de responsabilidades.

## Funcionalidades

- Cadastro de tarefas.
- Listagem de todas as tarefas.
- Busca de tarefas por ID.
- Filtro por status de conclusão.
- Atualização do status de uma tarefa.
- Exclusão de tarefas.
- Validação de dados.
- Tratamento de erros HTTP.
- Prevenção de títulos duplicados.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- Git e GitHub

## Estrutura do projeto

    api_tarefas/
    ├── routes/
    │   ├── __init__.py
    │   └── tarefas.py
    ├── schemas/
    │   ├── __init__.py
    │   └── tarefas.py
    ├── main.py
    ├── banco.py
    ├── requirements.txt
    └── .gitignore

O projeto utiliza APIRouter para organização dos endpoints e modelos Pydantic separados para validação dos dados de entrada e saída.

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| POST | /tarefas | Criar tarefa |
| GET | /tarefas | Listar tarefas |
| GET | /tarefas/{id} | Buscar tarefa específica |
| PATCH | /tarefas/{id}/status | Atualizar status |
| DELETE | /tarefas/{id} | Excluir tarefa |

## Como executar o projeto

**1. Instale as dependências:**

    python -m pip install -r requirements.txt

**2. Execute a aplicação:**

    python -m uvicorn main:app --reload

**3. Acesse a documentação interativa:**

    http://127.0.0.1:8000/docs

O banco de dados SQLite é criado automaticamente.

## Objetivo do projeto

Projeto desenvolvido para consolidar conhecimentos em desenvolvimento backend, APIs REST, bancos de dados relacionais, modularização com APIRouter e separação de responsabilidades.