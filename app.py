from classes.recomendacao_manga import RecomendacaoManga
from flask import request, jsonify, Flask, render_template
import os
import pandas as pd
import requests
dados = 'dados_mangar3.csv'
df = pd.read_csv(dados)
recomendacao = RecomendacaoManga(df)
app = Flask(__name__, template_folder='template')

API_KEY = 'AIzaSyBAkhcMOZ5Swyp26sGYWPJPaIVtwdioUqY'
SEARCH_ENGINE_ID = '41a01421b73d64c30'

def search_images(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&searchType=image&q={query}"
    response = requests.get(url)
    data = response.json()
    if 'items' in data:
        return data['items'][0]['link']
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recomendacoes', methods=['GET'])  # Definindo a rota corretamente
def obter_recomendacoes():
    nome_manga = request.args.get('nome_manga')
    if nome_manga:
        try:
            recomendacoes = recomendacao.get_recommendations(nome_manga)
            imagens = {}
            for manga in recomendacoes:
                imagem = search_images(f"{manga}")
                imagens[manga] = imagem
            return render_template('recomendacoes.html', recomendacoes=recomendacoes, imagens=imagens)
        except IndexError:
            return render_template('error.html')  # Renderiza a página de erro
    else:
        return jsonify({"error": "Por favor, forneça o parâmetro 'nome_manga' na consulta."})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
