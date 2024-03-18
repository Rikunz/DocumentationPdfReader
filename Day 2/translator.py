from deep_translator import GoogleTranslator

def translate_to_french(text):
    translated_text = GoogleTranslator(source='auto', target='fr').translate(text)
    return translated_text

english_text = "Hello, how are you?"
french_translation = translate_to_french(english_text)
print(french_translation)
