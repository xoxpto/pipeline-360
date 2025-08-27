[![CI](https://github.com/xoxpto/pipeline-360/actions/workflows/ci.yml/badge.svg)](https://github.com/xoxpto/pipeline-360/actions/workflows/ci.yml)

# Pipeline 360

Projeto base inicial.

## CLI

```bash
pipeline-360 --help
pipeline-360 hello --name "André"

# overrides de config
pipeline-360 --data-dir data_dev --log-level DEBUG --log-file logs/dev.log run --stage all

# limpar artefactos
pipeline-360 clean --yes
