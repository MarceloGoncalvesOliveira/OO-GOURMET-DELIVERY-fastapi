from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get('/api/hello')
def hello_world():
    '''
    endpoint que exibe uma mensagem incrivel do mundo 
    da programação

    '''
    return {'Hello': 'World'}

@app.get('/api/restaurantes/')
def get_restaurantes(restaurante: str = Query(None)):
    '''
    endepoint para ver os cardápios dos restaurantes
    
    '''
    url = 'https://guilhermeonrails.github.io/api-restaurantes/restaurantes.json'
    response = requests.get(url)

    if response.status_code == 200:
        dados_json = response.json()

        # Se nenhum restaurante for fornecido, retorna todos os dados
        if restaurante is None:
            return {'Dados': dados_json}

        # Filtra os dados do restaurante fornecido
        dados_restaurante = []
        for item in dados_json:
            if item['Company'] == restaurante:
                dados_restaurante.append({
                    "item": item['Item'],
                    "price": item['price'],
                    "description": item['description']
                })

        # Retorna os dados do restaurante ou uma mensagem de erro caso não exista
        if dados_restaurante:
            return {'Restaurante': restaurante, 'Cardapio': dados_restaurante}
        else:
            return {'Erro': f'O restaurante {restaurante} não foi encontrado.'}

    else:
        return {'Erro': f'{response.status_code} - {response.text}'}
