# 🚀 Pipeline 360

[![CI](https://github.com/xoxpto/pipeline-360/actions/workflows/ci.yml/badge.svg)](https://github.com/xoxpto/pipeline-360/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen)](#)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)

**Pipeline 360** é um projeto de **ETL simples** em Python com CLI, baseado em [Typer](https://typer.tiangolo.com/).  
Inclui logging configurável, configuração via `.env` e um pipeline modular de ingestão, transformação e exportação.

---

## ✨ Features

- ⚡ **CLI** (`pipeline-360`) com:
  - `run` → executa pipeline (`ingest → transform → export`)
  - `clean` → remove artefactos (`raw/`, `processed/`, `output/`)
  - `hello` → comando de teste
- ⚙️ **Configuração flexível**:
  - `.env` ou variáveis de ambiente
  - overrides por flags (`--data-dir`, `--log-level`, `--log-file`)
- 📜 **Logging configurável** (terminal ou ficheiro)
- ✅ **Testes automatizados** com `pytest` + GitHub Actions
- 🧹 **Qualidade de código** com **ruff** + **black**

---

## 📦 Instalação

# clonar repositório
git clone https://github.com/xoxpto/pipeline-360.git
cd pipeline-360

# criar ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# instalar dependências
pip install -r requirements.txt

---

## 🖥️ Uso da CLI

# ajuda geral
pipeline-360 --help

# exemplo: hello
pipeline-360 hello --name "André"

# correr pipeline completo
pipeline-360 run --stage all

# overrides de config
pipeline-360 --data-dir data_dev --log-level DEBUG --log-file logs/dev.log run --stage all

# limpar artefactos
pipeline-360 clean --yes

---

## 🧪 Testes

# correr testes unitários
pytest -q

# relatório de cobertura
pytest --cov=src --cov-report=term-missing

---

## 📂 Estrutura
pipeline-360/
├── src/pipeline_360/
│   ├── cli.py          # interface CLI (Typer)
│   ├── config.py       # gestão de settings/env
│   ├── logger.py       # configuração de logging
│   └── etl/            # ingest/transform/export
├── tests/              # testes unitários e integração
├── .github/workflows/  # CI/CD
└── README.md