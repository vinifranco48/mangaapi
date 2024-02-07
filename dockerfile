# Use a imagem base do Python
FROM python:3.11

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o código-fonte para o contêiner
COPY . .

# Instale as dependências do Python
RUN pip install -r requirements.txt

# Baixar dados NLTK durante a construção
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt


# Exponha a porta em que a aplicação Flask será executada
EXPOSE 5000



CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
