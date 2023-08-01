# import necesarry libraries
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


import openai
import json
openai.api_key = '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'
import mysql.connector

# connect with MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="test_maker_pro"
)


# get test
@app.route("/getTest",  methods =['POST'])

def getTest():

    # store messages with chatGPT
    messages = [ 
    {"role": "system", "content": 'Respond ONLY in with tests in a proper json format like {"questionNumber": {"question": question, "answerChoices": {"A": {"answerChoice": answerChoice, "correctAnswer": Bool}, "B": {"answerChoice": answerChoice, "correctAnswer": Bool}, "C": {"answerChoice": answerChoice, "correctAnswer": Bool}, "D": {"answerChoice": answerChoice, "correctAnswer": Bool}}, "explanation": detailed explanation for why other answerChoices aren\'t correct and why the correct answer is correct }}. Return ONLY json, no other text. Have only ONE correct answerChoice for each question' }
    ]

    # data from frontend
    data = request.get_json()

    # message to send to ChatGPT
    message = f"make a {data['type']} test"

    # ask chatGPT to give JSON test until it gives in proper format
    while True:
        try:
            messages.append({"role": "user", "content": message})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)  
            test = json.loads(chat.choices[0].message.content)

            break
        except:
            messages.append({"role": "system", "content": 'Make a PROPER test in a PROPER json format with 4 answer choices and only one correct answer with no other text' })
        
    messages.append({"role": "assistant", "content": chat.choices[0].message.content})

    # return JSON test
    return jsonify(test)


# signup
@app.route("/signup",  methods =['POST'])

def signup():

    # data from frontend
    data = request.get_json()
    mycursor = mydb.cursor()

    # check if user with same username exists
    mycursor.execute("SELECT userId FROM login where username = %s", (data['username'],))
    result = mycursor.fetchall()
    if len(result) > 0:
        return jsonify({'error': 'Username already exists'})
    else:

        # make new login if no user with same username exists 
        mycursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (data['username'], data['password']))
        mydb.commit()

    # return userId
    return jsonify({'userId': mycursor.lastrowid})


# login 
@app.route("/login",  methods =['POST'])

def login():

    # data from frontend
    data = request.get_json()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT userId FROM login where username = %s and password = %s", (data['username'], data['password']))
    result = mycursor.fetchall()

    # return userId
    if len(result) > 0:
        return jsonify({'userId': result[0][0]})
    else:
        return jsonify({'error': 'Username or Password incorrect'})

# save test 
@app.route("/saveTest",  methods =['POST'])

def saveTest():

    # data from frontend
    data = request.get_json()
    test = data['test']

    # insert test into MySQL database
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO tests (userId, testName, gottenCorrect) VALUES (%s, %s, %s)", (data['userId'], data['testName'], data['score']))
    testId = mycursor.lastrowid
    for key in test:
        mycursor.execute("INSERT INTO questions (testId, question, explanation) VALUES (%s, %s, %s)", (testId, test[key]['question'], test[key]['explanation']))
        questionId = mycursor.lastrowid
        for answerChoice in test[key]['answerChoices']:
            mycursor.execute("INSERT INTO answerchoices (questionId, answerChoice, correctAnswer) VALUES (%s, %s, %s)", (questionId, test[key]['answerChoices'][answerChoice]['answerChoice'], test[key]['answerChoices'][answerChoice]['correctAnswer']))

    print(test)
    mydb.commit()


    return 'ok'


# get saves tests list of user
@app.route("/getTests",  methods =['POST'])

def getTests():
    # data from frontend
    data = request.get_json()

    mycursor = mydb.cursor()
    mycursor.execute("select * from tests where userId = %s", (data['userId'],))
    result = mycursor.fetchall()

    return jsonify(result)


# get test info from database
@app.route("/getTestInfo",  methods =['POST'])

def getTestInfo():
    # data from frontend
    data = request.get_json()
    test = {}
    mycursor = mydb.cursor()

    # select all questions from database and add them to test
    mycursor.execute("select * from questions where testId = %s", (data['testId'],))
    results = mycursor.fetchall()

    for i, result in enumerate(results):
        test[i] = {'question': result[1], 'explanation': result[2], 'answerChoices': {}}
        mycursor.execute("select * from answerChoices where questionId = %s", (result[3],))
        answerChoices = mycursor.fetchall()
                
        # select all answer choices from database and add them to test
        for answerLetter, answerChoice in zip(['A', 'B', 'C', 'D'], answerChoices):
            test[i]['answerChoices'][answerLetter] = {'answerChoice': answerChoice[1], 'correctAnswer': True if answerChoice[2]=='1' else False}
    
    print(test)

    return  jsonify(test)


if __name__ == '__main__':
    app.run(debug = True)