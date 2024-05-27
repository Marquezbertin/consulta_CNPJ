import requests
import json
import pandas as pd
from datetime import datetime

# Função para consultar o CNPJ na primeira API
def consulta_cnpj_publica(cnpj):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Erro ao consultar a API Publica: {response.status_code}"}

# Função para consultar o CNPJ na segunda API
def consulta_cnpj_receitaws(cnpj):
    url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Erro ao consultar a API ReceitaWS: {response.status_code}"}

# Função para salvar os resultados em um arquivo TXT
def salvar_em_txt(data_hora_requisicao, data_hora_retorno, resultado_publica, resultado_receitaws):
    with open("resultado_consultas.txt", "a") as file:
        file.write(f"Data e hora da requisição: {data_hora_requisicao}\n")
        file.write(f"Data e hora do retorno: {data_hora_retorno}\n")
        file.write("Resultado da API Publica:\n")
        file.write(json.dumps(resultado_publica, indent=4))
        file.write("\n")
        file.write("Resultado da API ReceitaWS:\n")
        file.write(json.dumps(resultado_receitaws, indent=4))
        file.write("\n\n")

# Função para salvar os resultados em um arquivo JSON
def salvar_em_json(data_hora_requisicao, data_hora_retorno, resultado_publica, resultado_receitaws):
    data = {
        "data_hora_requisicao": data_hora_requisicao,
        "data_hora_retorno": data_hora_retorno,
        "resultado_publica": resultado_publica,
        "resultado_receitaws": resultado_receitaws
    }
    with open("resultado_consultas.json", "a") as file:
        json.dump(data, file, indent=4)
        file.write("\n")

# Função para combinar resultados de ambas APIs
def combinar_resultados(resultado_publica, resultado_receitaws):
    data = {
        "CNPJ": resultado_publica.get("cnpj", resultado_receitaws.get("cnpj", "")),
        "Razão Social": resultado_publica.get("razao_social", resultado_receitaws.get("nome", "")),
        "Status": resultado_publica.get("status", resultado_receitaws.get("situacao", "")),
        "Data de Abertura": resultado_publica.get("data_abertura", resultado_receitaws.get("abertura", "")),
        "Atividade": (resultado_publica.get("atividade_principal", [{}])[0].get("text", "")
                      if resultado_publica.get("atividade_principal") else "") or
                      (resultado_receitaws.get("atividade_principal", [{}])[0].get("text", "")
                      if resultado_receitaws.get("atividade_principal") else ""),
        "Telefone": resultado_publica.get("telefone", resultado_receitaws.get("telefone", ""))
    }
    return data

# Função para salvar os resultados em um arquivo Excel
def salvar_em_excel(data):
    df = pd.DataFrame([data])
    df.to_excel("resultado_consultas.xlsx", index=False)

# Função para ler dados do arquivo JSON e criar um Excel com cada linha representando uma coluna
def json_para_excel(json_file):
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    # Extrair os dados dos resultados
    dados = json_data["resultado_publica"]
    dados.update(json_data["resultado_receitaws"])

    # Transformar em DataFrame
    df = pd.DataFrame(dados.items(), columns=['Campo', 'Valor'])

    # Salvar em Excel
    df.to_excel("dados_json.xlsx", index=False)

# Função principal para realizar as consultas
def main(cnpj):
    data_hora_requisicao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    resultado_publica = consulta_cnpj_publica(cnpj)
    resultado_receitaws = consulta_cnpj_receitaws(cnpj)
    
    data_hora_retorno = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("Resultado da API Publica:")
    print(resultado_publica)
    
    print("\nResultado da API ReceitaWS:")
    print(resultado_receitaws)
    
    # Salvar resultados em TXT
    salvar_em_txt(data_hora_requisicao, data_hora_retorno, resultado_publica, resultado_receitaws)
    
    # Salvar resultados em JSON
    salvar_em_json(data_hora_requisicao, data_hora_retorno, resultado_publica, resultado_receitaws)

    # Combinar resultados e salvar em Excel
    dados_combinados = combinar_resultados(resultado_publica, resultado_receitaws)
    print("\nDados combinados:")
    print(dados_combinados)  # Verificação adicional dos dados combinados antes de salvar
    salvar_em_excel(dados_combinados)

    # Ler dados do arquivo JSON e criar Excel com cada linha como coluna
    json_para_excel("resultado_consultas.json")

if __name__ == "__main__":
    cnpj = "35679618000104"
    main(cnpj)
