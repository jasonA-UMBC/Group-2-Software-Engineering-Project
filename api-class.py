from urllib import response
from flask import Flask, jsonify            #import the necessary stuff from Flask
from supabase import create_client, Client
import os
from dotenv import load_dotenv

app = Flask(__name__)   
load_dotenv()
supabase: Client = create_client(os.getenv("SUPA_URL"), os.getenv("SUPA_KEY"))

def find_all_prereqs(class_code):
    #call the function to find the prerequsites from the class code
    #find_prereqs(class_code)
    return ['PH102.000, PH104.000']

@app.route('/schools', methods=['GET'])            #set up a page that lists all schools
def home():
    response = supabase.table("schools").select("*").execute()
    print(response.data)
    return response.data

@app.route('/sampleclasses', methods = ['GET'])     #metod to pull some sample classes
def sampleclasses():
    response = supabase.table("offerings").select("*").lt("offering_id", 1350).execute()
    print(response)
    return response.data

@app.route('/home/<int:num>', methods=['GET'])      #if the api is passed a /home/number, then return the square
def square(num):
    return jsonify({'data': num ** 2})


@app.route('/prereqs/<string:CC>', methods=['GET'])
def prereq(CC):
    data = find_all_prereqs(CC) #feed us a class, return all prereqs
    return jsonify({CC : data})

if __name__ == '__main__':              #run with debug
    app.run(debug=True)