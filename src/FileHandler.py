import PyPDF2
import re
import os
import bcrypt
import secrets
from flask import abort, Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from pymongo import MongoClient
from collections import Counter
from werkzeug.utils import secure_filename
import nltk
# import Authenticator
# from NLP_Analysis import TextAnalyzer
# from pymongo.errors import ServerSelectionTimeoutError
#from io import BytesIO

nltk.download('punkt')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

# connection string
client = MongoClient('mongodb+srv://killianm:VXnjHFL9nRTAFaYF@cluster0.tgc659u.mongodb.net/test')

def extract_text_from_pdf(pdf_file, pdf_filename):
    # Check to see if file format is correct
    file_extension = os.path.splitext(pdf_filename)[-1]
    if (file_extension != '.pdf'):
        abort(500, 'Unable to ingest non-pdf file format')
        # return False

    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    return text


def extract_paragraphs(text):
    paragraphs = text.split('\n\n')
    return [paragraph.strip() for paragraph in paragraphs if paragraph and paragraph.strip()]


def extract_keywords(text, num_keywords=None):
    # Tokenize words using a regular expression
    words = re.findall(r'\b\w+\b', text.lower())
    # Count word frequencies
    word_frequencies = Counter(words)
    # Get top # of keywords with their counts
    if num_keywords:
        keywords = {word: count for word, count in word_frequencies.most_common(num_keywords)}
    else:
        keywords = dict(word_frequencies)

    return keywords

def split_into_sentences(text):
    return nltk.sent_tokenize(text)


# def get_user_credentials():
#     email = input("Please enter your email: ")
#     password = input("Please enter your password: ")

#     # Hash Password for security
#     h_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#     return email, h_password


def upload_to_mongodb(database_name, collection_name, documents, user_info):
    db = client[database_name]
    collection = db[collection_name]

    result = collection.insert_one({**documents, **user_info})
    print(f"Inserted {result.inserted_id} documents into {database_name}.{collection_name}")

def check_credentials(email, password):
    db = client["PDFdb"]
    users_collection = db["Users"]

    user = users_collection.find_one({"Email": email})
    if user:
        # Compare the hashed password with the password from the form
        if bcrypt.checkpw(password.encode('utf-8'), user["Password"]):
            return True
    return False

def sign_up(email, password):
    db = client["PDFdb"]
    users_collection = db["Users"]

    user = users_collection.find_one({"Email": email})
    if not user:
        h_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_info = {"Email": email, "Password": h_password}
        users_collection.insert_one(user_info)
        return True
    return False

@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if check_credentials(email, password):
        session['logged_in'] = True
        session['email'] = email
        session['password'] = password
        return redirect(url_for('upload'))
    else:
        flash('Invalid email or password')
        return redirect(url_for('login'))
    
@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    if check_credentials(email, password):
        session['email'] = email
        session['password'] = password
        return redirect(url_for('upload'))
    else:
        flash('Invalid email or password')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route('/upload')
def upload():
    if 'logged_in' in session and session['logged_in']:
        return render_template('upload.html')
    else:
        flash('Please log in to access this page')
        return redirect(url_for('login'))

@app.route('/signup', methods=['POST'])
def signup_user():
    email = request.form['email']
    password = request.form['password']
    if sign_up(email, password):
        flash('Account created successfully')
    else:
        flash('Email already exists')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if check_credentials(email, password):
            session['logged_in'] = True
            session['email'] = email
            session['password'] = password
            return redirect(url_for('upload'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/handleUpload', methods=['POST'])
def handleUpload():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('upload'))

    if file:
        filename = secure_filename(file.filename)
        text = extract_text_from_pdf(file, filename)
        if text is False:
            flash("Unable to ingest file")
        else:
            flash("File ingested successfully and text is extracted. Yum.")

        paragraphs = extract_paragraphs(text)
        keywords_dict = extract_keywords(text)
        sentences = split_into_sentences(text)

        email = session.get('email')
        password = session.get('password')
        if not email or not password:
            flash("Please log in to access this feature.")
            return redirect(url_for('login'))
        
        user_info = {"Email": email, "Password": password}

        
        upload_to_mongodb("PDFdb", "Keywords", {"keyword": list(keywords_dict.keys())}, user_info)

        session['text'] = text
        session['paragraphs'] = paragraphs
        session['keywords'] = list(keywords_dict.keys())
        session['keywords_dict'] = keywords_dict
        session['sentences'] = sentences

        sorted_keywords = sorted(keywords_dict.items(), key=lambda x: x[1], reverse=True)

        return render_template('display_data.html', text=text, paragraphs=paragraphs, keywords=sorted_keywords, keywords_dict=keywords_dict, enumerate=enumerate)

    return redirect(url_for('upload'))

@app.route('/my_files')
def my_files():
    if 'logged_in' in session and session['logged_in']:
        # Get the user's email from the session
        email = session['email']
        
        # Query the MongoDB database to get all the files uploaded by this user
        db = client["PDFdb"]
        keywords_collection = db["Keywords"]
        files = list(keywords_collection.find({"Email": email}))

        # Render a template showing the list of files
        return render_template('my_files.html', files=files)
    else:
        flash('Please log in to access this page')
        return redirect(url_for('login'))

@app.route('/search_keyword', methods=['POST'])
def search_keyword():
    keyword = request.form['keyword'].lower()
    text = session.get('text', '')

    keyword_count = text.lower().count(keyword)
    return render_template('display_data.html', text=text, paragraphs=session.get('paragraphs', []), keywords=session.get('keywords', []), keyword=keyword, keyword_count=keyword_count)

@app.route('/word-info', methods=['GET'])
def word_info():
    word = request.args.get('word', '').strip().lower()
    if not word:
        return jsonify({"count": 0, "ranking": 0})

    keywords_dict = session.get('keywords_dict', {})
    count = keywords_dict.get(word, 0)
    sorted_keywords = sorted(keywords_dict.items(), key=lambda x: x[1], reverse=True)
    ranking = [i for i, kw in enumerate(sorted_keywords) if kw[0] == word]
    
    return jsonify({"count": count, "ranking": ranking[0] + 1 if ranking else 0})

@app.route('/sentences_with_word', methods=['GET'])
def sentences_with_word():
    word = request.args.get('word', '').strip().lower()
    if not word:
        return jsonify({"sentences": []})

    sentences = session.get('sentences', [])
    matching_sentences = [sentence for sentence in sentences if word in sentence.lower()]
    
    return jsonify({"sentences": matching_sentences})


if __name__ == "__main__":
    print("Starting Flask app. Visit http://127.0.0.1:5000/ to access the login page.")
    app.run(debug=True, port=5001)