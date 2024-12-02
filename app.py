from flask import Flask, render_template, request
import requests
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Função para obter conselhos da API
def get_advice():
    url = "https://api.adviceslip.com/advice"
    response = requests.get(url)
    return response.json()['slip']['advice']

# Função para traduzir os conselhos
def translate_advice(advice, target_language="pt"):
    return GoogleTranslator(source='en', target=target_language).translate(advice)

# Rota principal para exibir o menu e interagir com o usuário
@app.route("/", methods=["GET", "POST"])
def index():
    advices = []
    translated_advices = []
    
    if request.method == "POST":
        num_advice = int(request.form['num_advice'])
        
        # Recebe os conselhos da API
        advices = [get_advice() for _ in range(num_advice)]
        
        # Traduz os conselhos
        translated_advices = [translate_advice(advice) for advice in advices]
    
    # Passa as listas vazias se o formulário não foi enviado
    return render_template("index.html", advices=advices, translated_advices=translated_advices)

if __name__ == "__main__":
    app.run(debug=True)
