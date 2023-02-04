from flask import Flask, request
import json
from dbhelpers import run_statement

app = Flask(__name__)

# step into for debugger

# NOTEE YOU CAN NOT STORE ANY VARIABLES THAT PERSIST BETWEEN CALLS, IT ONLY EXISTS AS LONG AS
# THE FUNCTION RUNNING AFTER THE CALL
# BACK END IS NOT FOR LONG STORING DATA, THE ONLY THING RESPONSIBLE FOR STORING DATA LONG TERM
# (EG. FILES TOO) IS THE DATABASE.

# IMPORTANT
# request.args = FOR PARAMS ONLY (get)
# request.json = FOR DATA (post, patch, delete, etc)
@app.get('/api/book_length')
def get_book_length():
    length = request.args.get('minLength')
    if (length == None):
        length = 0
    result = run_statement("CALL get_book_length(?)", [length])
    if (type(result) == list):
        return json.dumps(result, default = str)
    else:
        return "There was an error! Try again."

@app.post('/api/author')
def post_author():
    author_name = request.json.get('authorName')
    author_dob = request.json.get('authorDob')
    # Here is where we're deciding these fields are mandatory
    if author_name == None:
        return "You must specify an author's name"
    if author_dob == None:
        return "You must specify an author's date of birth."
    result = run_statement("CALL post_author(?,?)", [author_name, author_dob])
    if result == None:
        return "Success"
    elif "Incorrect date value" in result:
        return "The date was invalid, please try again. Must be: yyyy-mm-dd"
    elif "Data too long for column 'name'" in result:
        return "The name must be longer than 4 and less than 50 characters."
    # elif "PUT CONSTRAINT NAME HERE FOR CHECKING CHARACTER LENGTH" in result:
    #     return "The name must be longer than 4 and less than 50 characters."

# Patch - takes name of author and dob, and fixed that authors dob to newly edited dob
@app.patch('/api/author')
def patch_author_dob():
    author_name = request.json.get('authorName')
    author_dob = request.json.get('authorDob')
    if author_name == None:
        return "You must specify an author's name"
    if author_dob == None:
        return "You must specify an author's date of birth."
    result = run_statement("CALL patch_dob(?,?)", [author_dob, author_name])
    if result == None:
        return "Success"
    elif "Incorrect date value" in result:
        return "The date was invalid, please try again. Must be: yyyy-mm-dd"
    elif "Data too long for column 'name'" in result:
        return "The name must be longer than 4 and less than 50 characters."

# Delete - delete req based on name (most times you will go by ID)
@app.delete('/api/author')
def delete_author():
    author_name = request.json.get('authorName')
    if author_name == None:
        return "You must specify an author's name"
    result = run_statement("CALL delete_by_author_name(?)", [author_name])
    if result == None:
        return "Success"
    else:
        return "Unable to delete author {}.".format(author_name)

@app.get('/api/books')
def get_books():
    result = run_statement("CALL get_books()")
    if (type(result) == list):
        return json.dumps(result, default=str)
    else: 
        return "Sorry, something went wrong."

@app.get('/api/books_authored')
def get_books_authored():
    result = run_statement("CALL author_book_count()")
    if (type(result) == list):
        return json.dumps(result, default=str)
    else: 
        return "Sorry, something went wrong."

@app.get('/api/best_selling_book')
def get_best_selling_book():
    result = run_statement("CALL get_best_seller()")
    if (type(result) == list):
        return json.dumps(result, default=str)
    else: 
        return "Sorry, something went wrong."

@app.get('/api/best_selling_author')
def get_best_selling_author():
    result = run_statement("CALL best_selling_author()")
    if (type(result) == list):
        return json.dumps(result, default=str)
    else: 
        return "Sorry, something went wrong."

app.run(debug = True)