# Consulta CNPJ Script

Este script realiza consultas de CNPJ utilizando duas APIs diferentes e salva os resultados em arquivos TXT, JSON e Excel. 

Esse script pode ser utilizado como teste para validar se a API integrada ao seu sistema está funcionando. Neste exemplo utilizamos duas API´s, porem voce pode trocar os links e realizar a consulta.  

## Funcionalidades

- Consulta informações de CNPJ em duas APIs:
  - [API Pública](https://publica.cnpj.ws/)
  - [ReceitaWS](https://receitaws.com.br/)
- Salva os resultados das consultas em arquivos nos formatos TXT, JSON e Excel.
- Combina os resultados das duas APIs em um formato unificado.

## Requisitos

- Python 3.6+
- Bibliotecas Python:
  - `requests`
  - `json`
  - `pandas`
  - `datetime`

