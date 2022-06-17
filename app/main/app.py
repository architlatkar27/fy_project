from crypt import methods
from flask import Flask,request
import json
import index
from threading import Thread
import threading
app = Flask(__name__)

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


root = 0 # initialize root with index tree root. maybe for now we can move the init part over here.

def initializer():
    pass

@app.route('/test', methods=['GET'])
def test():
    '''
    test
    '''
    print("success")
    return "success 200 main"

@app.route('/execute', methods=['GET'])
def query_collector():
    '''
    Recieve query string
    call function to get node list
    call function to send request to all nodes and collect all the responses and send back
    return the consolidated response
    '''
    data = request.form
    nodes = nodeSelector(data)
    answer = consildator(data, nodes)
    return json.dumps(answer)
    pass

def nodeSelector(data):
    '''
    Recieve a request, use the index to determine subset of nodes to send the data to.
    '''
    value = data[0] # check how to get the data.
    x = index.BTree.search_key(root, value)
    return x.nodes

def consildator(data, nodes):
    '''
    asynchronously send requests to all the nodes, collect response and consolidate in one
    '''
    req_threads = []
    for i, x in enumerate(nodes):
        req_threads.append(ThreadWithReturnValue(target=query_forward, args=(data, x)))
        req_threads[i].start()
    answers = []
    for x in req_threads:
        answers.append(x.join())
    
    # need to see how to combine the answers returned over here
    return answers

def query_forward(data, node):
    '''
    forward query to individual node and give back the response
    '''
    # send request to single node app


if __name__ == '__main__':
    print("starting main...")
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host="0.0.0.0", port=8080, debug=True)