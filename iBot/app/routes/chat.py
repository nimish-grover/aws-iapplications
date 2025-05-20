import json
from flask import current_app, render_template, request, session
from flask_smorest import Blueprint
import requests

blp = Blueprint('chat', 'chat', description="Chat with OpenAI API")

def get_chatgpt_message(messages, URL, model="gpt-3.5-turbo"):
    payload = {
        "model": model,
        "messages": messages,
        "temperature" : 0.7,
        "top_p":1.0,
        "n" : 1,
        "stream": True,  # Set stream to True for streaming response
        "presence_penalty":0,
        "frequency_penalty":0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {current_app.config['OPENAI_API_KEY']}"
    }

    response = requests.post(URL, headers=headers, json=payload, stream=True)  # Set stream=True here
    return response

@blp.route('/', methods=['GET', 'POST'])
def ai_response():
    SYSTEM_PROMPT = "You are a waterbot named JiM. 'J' stands for Jal (meaning water in English), 'M' stands for Mission, and 'i' represents your intellect. Introduce yourself as JiM and share your name to others as JiM. You are designed to provide information on water, water conservation structures, natural resource management (NRM) works, Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA), watershed development, and related areas. You are equipped to use thematic maps for developing gram panchayat plans in India to execute NRM works under MGNREGA scheme. If asked questions outside this scope, inform the user to contact Mr. Krishan Tyagi, Project Manager, Project WASCA II.\n\n"
    api_url = current_app.config["OPENAI_API_URL"]
    chat = {'user_message': '', 'bot_message': '', 'token_count': 0 }

    if request.method == 'POST':
        user_message = request.form['user_message']
        if session.get('chats'):
            chats = session.get('chats')
            messages = session.get('messages')
            token_count = chats[len(chats)-1]['token_count']
        else:
            chats = []
            messages = []
            token_count = 0
            messages.append({'role': 'system', 'content': SYSTEM_PROMPT})

        if len(chats) > 5:
            chat['user_message'] = user_message
            chat['bot_message'] = 'You have reached your free limits. Please contact the administrator for further details.'
            chats.append(chat)
        else:
            if user_message:
                messages.append({'role': 'user', 'content': user_message})
                response = get_chatgpt_message(messages, api_url)
                
                # Iterate through streaming response
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        message_content = json.loads(chunk.decode('utf-8'))
                        assistant_message = message_content["choices"][0]["message"]["content"]
                        token_count += message_content["usage"]["total_tokens"]
                        messages.append({'role': 'assistant', 'content': assistant_message})
                        chat['user_message'] = user_message
                        chat['bot_message'] = assistant_message
                        chat['token_count'] = token_count + sum(chat['token_count'] for chat in chats)
                        chats.append(chat)
                        session['chats'] = chats
                        session['messages'] = messages
                        
                        # Send the chunked response to the client
                        yield chunk
                
        session['chats'] = chats
        session['messages'] = messages
        return render_template('chats.html', chats=chats)
    else:
        session.clear()
    return render_template('chats.html')
