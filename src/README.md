# PDF NLP Application

The PDF NLP Application is a web-based tool for processing and analyzing PDF documents using natural language processing techniques. The application allows users to upload PDF documents, extract text and keywords, search for specific words within the document, and navigate sentences containing the searched word.

## Table of Contents

- [Features](#features)
- [APIs](#apis)
- [Architecture](#architecture)
- [Installation](#installation)
  - [Docker](#docker)
  - [Manual Installation](#manual-installation)
- [Usage](#usage)
- [Tests](#tests)

## Features

- Upload PDF documents
- Extract and display text from the PDF document
- Display a list of keywords sorted by their rank of occurrences
- Search for specific words within the document
- Navigate through sentences containing the searched word

## APIs

The application has the following API endpoints:

1. `/upload`: Accepts a PDF file as input and processes the text and keywords from the file.
2. `/word-info`: Accepts a word as a query parameter and returns the count and ranking of the word within the uploaded document.
3. `/sentences_with_word`: Accepts a word as a query parameter and returns a list of sentences containing the word in the document.

## Architecture

The application is built using Python with the Flask web framework. The frontend is developed using HTML, CSS, and JavaScript. The backend uses the PyPDF2 library to extract text from the PDF files, and the NLTK library to process and analyze the text using natural language processing techniques.

The application is organized into the following components:

- `app.py`: The main Flask application file.
- `templates/`: The directory containing the HTML templates.
- `static/`: The directory containing static files, such as CSS and JavaScript files.

## Installation

### Docker

To run the application using Docker, follow these steps:

1. Install [Docker](https://www.docker.com/) on your machine.
2. Clone the repository: `git clone https://github.com/yourusername/pdf-nlp-application.git`
3. Navigate to the project directory: `cd pdf-nlp-application`
4. Build the Docker image: `docker build -t pdf-nlp-application .`
5. Run the Docker container: `docker run -p 5000:5000 pdf-nlp-application`
6. Access the application at `http://localhost:5000`

### Manual Installation

To manually install and run the application, follow these steps:

1. Install [Python 3](https://www.python.org/downloads/) on your machine.
2. Clone the repository: `git clone https://github.com/yourusername/pdf-nlp-application.git`
3. Navigate to the project directory: `cd pdf-nlp-application`
4. Install the required packages: `pip install -r requirements.txt`
5. Run the application: `python app.py`
6. Access the application at `http://localhost:5000`

## Usage

1. Access the application at `http://localhost:5000`
2. Upload a PDF document using the upload form.
3. Use the 'Toggle Text' button to display the extracted text from the PDF.
4. Use the 'Toggle Keywords' button to display a table of keywords sorted by their rank of occurrences.
5. Enter a word in the 'Word:' input field and click 'Get word info' to display the count and ranking of the word within the document.
6. Use the arrow buttons to navigate through sentences containing the searched word.

## Tests

To run the tests for this application, follow these steps:

1. Ensure that you have `pytest` installed. If it's not already installed, you can install it using pip:

```bash
pip install pytest
```

2. Utilize the file `test_FileHandler.py` to run tests on `FileHandler.py`. You can add more tests to the `test_FileHandler.py` file as needed to cover other functions and scenarios in your `FileHandler.py` code.

3. To run the tests, open a terminal/command prompt, navigate to your project directory, and run this command:

```bash
pytest

# OR

pytest test_FileHandler.py
```
