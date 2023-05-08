import spacy
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Initializing the ability to process the text with spacy
nlp = spacy.load('en_core_web_sm')

class TextAnalyzer(Resource):

    # For the text analyzer it should check
    # - if there is content in the file
    # - analyze stats: # words, # of sentences, # of entities
    # - Save results and upload to the API

    def post(self):
        # Parse the request body
        data = request.json
        if not data or 'text' not in data:
            return {
                'status': 'error',
                'message': 'Invalid request body'
                }, 400
        
        text = data['text']
        
        # Using spacy to analyze text
        doc = nlp(text)
        
        # Aquire stats of the text
        num_words = 0
        # 'len(doc)' includes punctuation, get word count thru a for loop
        for tokens in doc:
            if not tokens.is_punct:
                num_words += 1
        num_sentences = len(list(doc.sents))
        num_entities = len(doc.ents)
        
        # Return the analysis results
        return {
            'status': 'success', 
            'data': {
                'num_words': num_words,
                'num_sentences': num_sentences,
                'num_entities': num_entities}
                }, 200

# Add the TextAnalyzer resource to the API
api.add_resource(TextAnalyzer, '/analyze')

if __name__ == '__main__':
    app.run(debug=True)
