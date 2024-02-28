from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from unidecode import unidecode
from classes.editdistance import Edit_Distance_Custom

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
        # Calcula as distâncias de edição entre o nome fornecido e todos os nomes na base de dados
        distances = [Edit_Distance_Custom(name_lower_normalized, self.preprocess_text(manga_name)).distance() for manga_name in self.df['Nome Processado']]
        # Encontra o índice do mangá com o menor valor de distância de edição
        idx = distances.index(min(distances))
        # Obtém as pontuações de similaridade para todos os mangás
        sim_scores = list(enumerate(self.cosine_similarities[idx]))
        # Ordena as pontuações em ordem decrescente
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Seleciona os 5 principais mangás (excluindo o próprio mangá)
        sim_scores = sim_scores[1:6]
        # Obtém os índices dos mangás recomendados
        manga_indices = [i[0] for i in sim_scores]
        # Retorna os nomes dos mangás recomendados
        return self.df['Nome'].iloc[manga_indices]