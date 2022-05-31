from crypt import methods
from flask import Flask,request

app = Flask(__name__)

@app.route('/execute', methods=['GET'])
def query_collector():
    '''
    Recieve query string, search the index and then send the query to destination nodes
    '''
    
    
    pass