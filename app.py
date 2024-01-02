from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ler_planilha_excel(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)
    return df

def criar_diretorio_uploads():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return "API Flask para ler planilha Excel."

@app.route('/descricao_planilha', methods=['POST'])
def obter_descricao_planilha():
    criar_diretorio_uploads()

    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
        # Salva o arquivo no diretório de uploads
        caminho_arquivo_excel = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(caminho_arquivo_excel)

        # Lê a planilha Excel
        df = ler_planilha_excel(caminho_arquivo_excel)

        # Obtém a coluna 'Descrição'
        descricao_coluna = df['Descrição'].tolist()

        return jsonify(descricao_coluna)

    return jsonify({"error": "Invalid file format"})

if __name__ == '__main__':
    app.run(debug=True)
