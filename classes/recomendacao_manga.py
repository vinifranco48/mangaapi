from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from unidecode import unidecode

class RecomendacaoManga:
    def __init__(self, dados):
        self.df = self.preprocess_dataframe(dados)
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['Descrição Processada'])
        self.cosine_similarities = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

    def preprocess_text(self, text):
        text = unidecode(text)  # Remove acentos
        tokens = word_tokenize(text.lower())  # Tokenização e minúsculas
        tokens = [token for token in tokens if token.isalpha() and token not in self.stop_words_pt]  # Remoção de stopwords e não alfanuméricos
        return ' '.join(tokens)

    def preprocess_dataframe(self, df):
        self.stop_words_pt = set(stopwords.words('portuguese'))  # Carrega stopwords em português
        df['Descrição Processada'] = df['Descrição'].apply(lambda x: self.preprocess_text(x))  # Aplica a função preprocess_text à coluna 'Descrição'
        df['Nome Processado'] = df['Nome'].apply(lambda x: self.preprocess_text(x))  # Adiciona uma nova coluna 'Nome Processado' ao DataFrame
        return df

    def get_recommendations(self, name):
        name_lower = name.lower()  # Converte o nome fornecido para minúsculas
        name_lower_normalized = self.preprocess_text(name_lower)  # Normaliza o nome fornecido
        idx = self.df.index[self.df['Nome Processado'] == name_lower_normalized].tolist()[0]  # Encontra o índice do mangá com o nome fornecido
        sim_scores = list(enumerate(self.cosine_similarities[idx]))  # Obtém as pontuações de similaridade para todos os mangás
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # Ordena as pontuações em ordem decrescente
        sim_scores = sim_scores[1:6]  # Seleciona os 5 principais mangás (excluindo o próprio mangá)
        manga_indices = [i[0] for i in sim_scores]  # Obtém os índices dos mangás recomendados
        return self.df['Nome'].iloc[manga_indices]  # Retorna os nomes dos mangás recomendados
