
from flask import Flask, request, jsonify, render_template
import os
import dialogflow_v2 as dialogflow
import requests
import json

GOOGLE_APPLICATION_CREDENTIALS="tracybikeshop-jxmpua-da11dd22298d.json"
DIALOGFLOW_PROJECT_ID="tracybikeshop-jxmpua"


app = Flask(__name__)

@app.route('/')
def Welcome():
    return render_template('index.html')
    #return 'this works!'
    #app.send_static_file('index.html')
    
def detect_intent_texts(project_id, session_id, text, language_code):
    #create an instance of dialogflow
    session_client = dialogflow.SessionsClient()
    #set API with credentials
    session = session_client.session_path(project_id, session_id)
    
    #if text is valid get chatbot feedback
    if text:
        #format text from user
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        #input formatted text to chatbot
        query_input = dialogflow.types.QueryInput(text=text_input)
        #generate text response to user 
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        #return fulfillment text to end user
        return response.query_result.fulfillment_text

@app.route('/send_message', methods=['POST'])
def send_message():

    #get user text from form element
    message = request.form['message']
    #get project id from dialogflow
    project_id = DIALOGFLOW_PROJECT_ID
    #get and format response to user from dialogflow
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    #format response text for user
    response_text = { "message":  fulfillment_text }                
    return jsonify(response_text)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= GOOGLE_APPLICATION_CREDENTIALS
port = os.getenv('PORT', '5003')
if __name__ == "__main__":
	app.run(debug=True, port=int(port))