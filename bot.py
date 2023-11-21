from flask import Flask, request
import settings 
import services

app = Flask(__name__)

@app.route('/welcome', methods=['GET'])
def  welcome():
    return 'Hola guardias ?)'

@app.route('/webhook', methods=['GET'])
def token_verification():

    try:

        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == settings.token and challenge != None:
            return challenge
        else:
            return 'Incorrect Token', 403
        
    except Exception as e:

        return e, 403
    
@app.route('/webhook', methods=['POST'])
def message_received():

    try:
    
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.get_wa_message(message)

        services.chatbot_options(text, number,messageId,name)
        return 'sent'

    except Exception as e:

        return 'error while sending ' + str(e)

if __name__ == '__main__':
    app.run()