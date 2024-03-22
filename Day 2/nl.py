import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('punkt')

english_text = "Hello, How are you today? i am looking for a pizza, do yoou know where to get that, ahhh i am so hungry right now, hope fully i can get my pizza as soon as possible."
french_text = "Bonjour, Comment allez-vous aujourd'hui ? Je cherche une pizza, savez-vous où la trouver, ahhh j'ai tellement faim en ce moment, j'espère vraiment que je pourrai avoir ma pizza le plus tôt possible."

english_tokens = word_tokenize(english_text.lower())
french_tokens = word_tokenize(french_text.lower())

stop_words = set(stopwords.words('english') + stopwords.words('french'))
english_tokens = [word for word in english_tokens if word.isalnum() and word not in stop_words]
french_tokens = [word for word in french_tokens if word.isalnum() and word not in stop_words]

english_text_cleaned = ' '.join(english_tokens)
french_text_cleaned = ' '.join(french_tokens)

combined_texts = [english_text_cleaned, french_text_cleaned]

# Calculate TF-IDF vectors
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(combined_texts)

# Calculate cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

print("Cosine similarity between English and French text:", cosine_sim[0][0])