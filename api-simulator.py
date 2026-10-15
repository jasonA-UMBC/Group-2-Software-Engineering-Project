from flask import Flask, jsonify            #this does require flask to be installed (pip install flask)
import random

#list of simulated course codes
#Note that these course codes may or may not be real, I made them up
#However, the format is correct. JHU codes are formatted as such:
#2 letter department code,
#3 digit class code,
#3 digit section code. This section code is only relevant for scheduling,
#as it's relevant to the specific time. It does not affect any prerequisites. 
course_code_data = ['AS101','RF999','RF923','BO875', 
                    'PF315','PL229','LO002','DY616',
                    'HU740','FD004','JD876','GV963',
                    'PP671','VB098','HH123','NG123',
                    'PL085','GF653','GFD24','PO546'
        ]              

app = Flask(__name__)

@app.route('/', methods=['GET'])            #set up a hello world landing page
def home():
    return jsonify({'data': 'hello world'})

@app.route('/prereqs/<string:CC>', methods=['GET'])
def prereq(CC):
    data = []
    if(CC in course_code_data):
        count = random.randint(0,5)                         #generate up to 5 random numbers, and get
        random_numbers = random.sample(range(0,20), count)  #the corresponding course codes. 
        data = [course_code_data[i] for i in random_numbers]
        if CC in data:
            data.remove(CC)                             #ensure that no course can have itself as a prerequisite
    else:
        data = ["ERROR: COURSE CODE NOT FOUND"]         #if the course code is not in the above list, then
    return jsonify({CC : data})                         #return that the course cannot be found. 


if __name__ == '__main__':              #run with debug
    app.run(debug=True)