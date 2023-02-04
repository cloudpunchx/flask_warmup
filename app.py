from flask import Flask
import json
from dbhelpers import run_statement

app = Flask(__name__)

@app.get('/api/books')
def get_books():
    result = run_statement("CALL get_books()")
    if (type(result) == list):
        result_json = json.dumps(result, default=str)
        return result_json
    else: 
        return "Sorry, something went wrong."

@app.get('/api/books_authored')
def get_books_authored():
    result = run_statement("CALL author_book_count(?)", ['Grady Hendrix'])
    if (type(result) == list):
        result_json = json.dumps(result, default=str)
        return result_json
    else: 
        return "Sorry, something went wrong."

@app.get('/api/best_selling_book')
def get_best_selling_book():
    result = run_statement("CALL get_best_seller()")
    if (type(result) == list):
        result_json = json.dumps(result, default=str)
        return result_json
    else: 
        return "Sorry, something went wrong."

@app.get('/api/best_selling_author')
def get_best_selling_author():
    result = run_statement("CALL best_selling_author()")
    if (type(result) == list):
        result_json = json.dumps(result, default=str)
        return result_json
    else: 
        return "Sorry, something went wrong."

app.run(debug = True)