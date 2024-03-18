import spacy

# Load the English and French language models
nlp_en = spacy.load('en_core_web_sm')
nlp_fr = spacy.load('fr_core_news_sm')

# Function to translate text from English to French
def translate_en_to_fr(text):
    # Parse the English text
    doc_en = nlp_en(text)
    
    # Initialize an empty list to store the French translations
    translations_fr = []
    
    # Iterate over the tokens in the English text
    for token in doc_en:
        # Translate each token to French and append to the list
        translations_fr.append(token.text if token.text in nlp_fr.vocab.strings else token.lemma_)
    
    # Join the translated tokens to form the translated text
    translated_text = ' '.join(translations_fr)
    
    return translated_text

# Example usage
english_text = "Hi, Welcome Home?"
translated_text = translate_en_to_fr(english_text)
print("English:", english_text)
print("French:", translated_text)