from flask import Flask, jsonify            #import the necessary stuff from Flask
app = Flask(__name__)                       

@app.route('/', methods=['GET'])            #set up a hello world landing page
def home():
    return jsonify({'data': 'hello world'})

@app.route('/home/<int:num>', methods=['GET'])      #if the api is passed a /home/number, then return the square
def disp(num):
    return jsonify({'data': num ** 2})

if __name__ == '__main__':              #run with debug
    app.run(debug=True)