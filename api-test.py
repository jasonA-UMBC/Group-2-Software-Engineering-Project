from flask import Flask, jsonify            #import the necessary stuff from Flask
#import database.py/jhu api                 #import whatever database/api calls we need
app = Flask(__name__)   

def find_all_prereqs(class_code):
    #call the function to find the prerequsites from the class code
    #find_prereqs(class_code)
    return ['PH102.000, PH104.000']

@app.route('/', methods=['GET'])            #set up a hello world landing page
def home():
    return jsonify({'data': 'hello world'})

@app.route('/home/<int:num>', methods=['GET'])      #if the api is passed a /home/number, then return the square
def square(num):
    return jsonify({'data': num ** 2})


@app.route('/prereqs/<string:cl>', methods=['GET'])
def prereq(cl):
    data = find_all_prereqs(cl)
    return jsonify({cl : data})

if __name__ == '__main__':              #run with debug
    app.run(debug=True)


    #feed us a class, return all prereqs
