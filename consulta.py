import requests
import json
import pandas

def converter_data(dia):
    dia = dia[8:]+"/"+dia[5:7]+"/"+dia[0:4]
    print("Última atualização dos dados:", dia)
    return dia

def chave_acesso(chave="5d0eb200bb9fb42872430c207728160f"):
    return "http://data.fixer.io/api/latest?access_key="+chave

def converter_em_reais(valor_real, valor_estrangeiro):
    return round(valor_real/valor_estrangeiro, 2)

def exportar_tabela(lista_titulos, lista_valores, nome_arquivo, lista_dia):
    celulas = pandas.DataFrame({'Moedas':lista_titulos, 'Valores':lista_valores,
    'Acessado em':lista_dia})
    celulas.to_csv(nome_arquivo+".csv",index=False, sep=";")
    print("Tabela exportada com sucesso!")

def main():
    chave = input("Informe a chave de acesso do Fixer.io, se não tiver, aperte enter")
    url = chave_acesso(chave) if len(chave) > 0 else chave_acesso()
    print("Acessando base de dados...")
    resposta = requests.get(url)
    if resposta.status_code == 200:
        print("Conexão com a base de dados estabelecida com sucesso...")
        dados = resposta.json()
        dia_convertido = converter_data(dados['date'])
        euro_em_reais = converter_em_reais(dados['rates']['BRL'], dados['rates']['EUR'])
        bitcoin_em_reais = converter_em_reais(dados['rates']['BRL'], dados['rates']['BTC'])
        dollar_em_reais = converter_em_reais(dados['rates']['BRL'], dados['rates']['USD'])
        escolha = input("Digite:\nB - Bitcoin\nD - Dollar\nE - Euro\nA - Todas: ").upper()
        if(escolha == 'B'):
            exportar_tabela(['Bitcoin'], [bitcoin_em_reais], 'bitcoin', [dia_convertido])
        elif(escolha == 'D'):
            exportar_tabela(['Dollar'], [dollar_em_reais], 'dollar', [dia_convertido])
        elif(escolha == 'E'):
            exportar_tabela(['Euro'], [euro_em_reais], 'euro', [dia_convertido])
        elif(escolha == 'A'):
            exportar_tabela(['Bitcoin', 'Dollar', 'Euro'], [bitcoin_em_reais, dollar_em_reais, euro_em_reais], 'moedas', [dia_convertido, '', ''])
        else:
            print("Você não esolheu nenhuma das opções. Sua tabela não será exportada!")
    else:
        print("Erro ao acessar a base de dados")

if __name__ == '__main__':
    main()