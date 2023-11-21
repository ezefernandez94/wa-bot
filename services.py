import requests
import settings
import json
import time

def get_wa_message(message):
    if 'type' not in message :
        text = 'unknown message type'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = "message coudn't be processed"
    
    
    return text

def send_wa_message(data):
    
    try:

        whatsapp_token = settings.whatsapp_token
        whatsapp_url = settings.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        
        print("sending ..  ", data)

        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'message sent', 200
        else:
            print('RIP')
            return 'error when trying to send the message', response.status_code
    
    except Exception as e:

        return e, 403
    
def text_message(number,text):
    
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )

    return data

def button_reply_message(number, options, body, footer, sedd, messageId):

    buttons = []

    for iteration, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(iteration+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )

    return data

## Example function for list reply
def list_reply_message(number, options, body, footer, sedd, messageId):
    
    rows = []
    
    for iteration, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(iteration+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )

    return data

def document_message(number, url, caption, filename):
    
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )

    return data

def get_media_id(media_name , media_type):

    media_id = ""

    if media_type == "image":
        media_id = settings.images.get(media_name, None)
    elif media_type == "video":
        media_id = settings.videos.get(media_name, None)
    elif media_type == "audio":
        media_id = settings.audio.get(media_name, None)
    elif media_type == "xlsx":
        media_id = settings.xlsx.get(media_name, None)
    elif media_type == "pdf":
        media_id = settings.pdf.get(media_name, None)

    return media_id

def reply_text_message(number, messageId, text):

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )

    return data

def mark_as_read_message(messageId):

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )

    return data

def chatbot_options(text,number, messageId, name):

    ## text = text.lower()
    list = []

    print("User message: ",text)

    mark_as_read = mark_as_read_message(messageId)

    list.append(mark_as_read)

    time.sleep(2)

    ## Hospital Services
    services = ['Cardiología', 'Terapia', 'Gastroenterología', 'Imagenes']
    contacts = ['Elcar Diologo', 'Elte Rapista', 'Lagastro Enterologa', 'Elima Gista']
    contact_numbers = ['1111-1111', '2222-2222', '3333-3333', '4444-4444']
    
    if text not in services:
        
        if "hola" in text:

            body = "¡Hola! 👋 ¿Qué servicio deseas conocer?"
            footer = "Equipo CityHaters"

            response_msg = button_reply_message(number, services, body, footer, "sed1", messageId)
            
            list.append(response_msg)

        else:

            response_msg = text_message(number, 'No conozco este servicio. por favor, intente nuevamente')
            list.append(response_msg)

    else:

        service_index = services.index(text)
        data = text_message(number, "El médico de guardia para el día de hoy en el servicio de {} es {} y \
                            su número de contacto es: {}".format(services[service_index],
                                                                 contacts[service_index],
                                                                 contact_numbers[service_index])
                            )
        list.append(data)

    for item in list:
        send_wa_message(item)

## Correct number to avoid sending errors .. we might have a problem with foreign numbers, if any (?)
def replace_start(phone_number):
    if phone_number.startswith("549"):
        return "54" + phone_number[3:]
    else:
        return phone_number