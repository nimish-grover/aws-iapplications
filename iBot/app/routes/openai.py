import json
from flask import current_app, render_template, request, session, stream_with_context
from flask_smorest import Blueprint
import requests
import textwrap
from IPython.display import display
from IPython.display import Markdown
import tiktoken
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as PC
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


blp = Blueprint('openai', 'openai', description="Communication using open ai api")

api_url = ""
def get_chatgpt_message(messages, URL, model="gpt-3.5-turbo"):
    payload = {
            "model": model,
            "messages": messages,
            "temperature" : 0.7,
            "top_p":1.0,
            "n" : 1,
            "stream": False,
            "presence_penalty":0,
            "frequency_penalty":0,
            }

            # set the headers
    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {current_app.config['OPENAI_API_KEY']}"
            }

            # send the request to API
    response = requests.post(URL, headers=headers, json=payload, stream=False)
    return response

@blp.route('/jim', methods=['GET', 'POST'])
def ai_response():
    SYSTEM_PROMPT = '''
    You are a waterbot named JiM. 'J' stands for Jal (meaning water in English), 'M' stands for Mission, and 'i' represents your intellect. 
    Introduce yourself as JiM and share your name to others as JiM. You are designed to provide information on water, water conservation 
    structures, natural resource management (NRM) works, Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA), watershed development, 
    and related areas. You are equipped to use thematic maps for developing gram panchayat plans in India to execute NRM works under 
    MGNREGA scheme. If asked questions outside this scope, inform the user to connect with WASCA team and then try to answer the question 
    according to the best of your capability.\n\n"    
    '''
    api_url = current_app.config["OPENAI_API_URL"]
    chat = {'user_message': '','bot_message':'', 'token_count': 0 }
    
    if request.method == 'POST':
        user_message = request.form['user_message']
        # Check if the chats already exist
        if session.get('chats'):
            chats = session.get('chats')
            messages = session.get('messages')
            token_count = chats[len(chats)-1]['token_count']
        # else create new list for chats (sent to template) and messages (sent to openai)
        else:
            chats = []
            messages = []
            token_count = 0
            messages.append({'role':'system','content':SYSTEM_PROMPT})
        # cap the upper limit of free messages to 10 only. 
        if len(chats)>5:
            chat['user_message']=user_message
            chat['bot_message']='You have reached your free limits. Please contact the administrator for further details.'
            chats.append(chat)
        else:
            if user_message:
                messages.append({'role':'user', 'content':user_message})
                response = get_chatgpt_message(messages, api_url)
                message_content = json.loads(response.text)
                assistant_message = message_content["choices"][0]["message"]["content"]
                token_count = token_count + message_content["usage"]["total_tokens"]
                messages.append({'role':'assistant','content': assistant_message})
                chat['user_message']=user_message
                chat['bot_message']=assistant_message
                chat['token_count']= token_count + sum(chat['token_count'] for chat in chats)
                chats.append(chat)
        
        session['chats'] = chats
        session['messages']=messages   
        return render_template('chat.html', chats = chats)
        # return render_template('chat.html')
    else:
        session.clear()
    return render_template('chat.html')

@blp.route('/rag', methods=['GET', 'POST'])
def rag():
    # define the pinecode index and chat object    
    pinecone_index = 'mgnrega'
    chat = {'user_message': '','bot_message':'', 'token_count': 0 }

    # check if the user submitted the question
    if request.method == 'POST':
        user_message = request.form['user_message']
        # Fill chats or initialize 
        if session.get('chats'):
            chats = session.get('chats')
            messages = session.get('messages')
            token_count = chats[len(chats)-1]['token_count']
        # else create new list for chats (sent to template) and messages (sent to openai)
        else:
            chats = []
            messages = []
            token_count = 0
            # messages.append({'role':'system','content':SYSTEM_PROMPT})
        # declare the openai variables
        llm = OpenAI()
        embeddings = OpenAIEmbeddings()
        # use the openai to query pinecone
        docsearch = PC.from_existing_index(pinecone_index, embeddings) # get the pinecone embeddings
        retrieve_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever()) # declrate the retrieval engine
        docs = docsearch.similarity_search(user_message, k=2) # give atleast two source references 
        bot_message = retrieve_qa.run(user_message) # retreive the response based on user query

        chat['user_message']=user_message
        chat['bot_message']= bot_message
        chat['token_count'] = 0

        chats.append(chat)

        session['chats'] = chats
        # session['messages']=messages

        return render_template('chat.html', chats=chats, docs=docs)
    else:
        session.clear()
    return render_template('chat.html')

@blp.route('/chats', methods=['GET', 'POST'])
def openai_response():
    SYSTEM_PROMPT = "You are a waterbot named JiM. Introduce yourself as JiM. You are designed to provide information on water, water conservation structures, natural resource management (NRM) works, Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA), watershed development, and related areas. You are equipped to use thematic maps for developing gram panchayat plans in India to execute NRM works under MGNREGA scheme. If asked questions outside this scope, inform the user to contact the competent authority.\n\n"
    # api_url = app.config["OPENAI_API_URL"]
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
                response = get_chatgpt_message(messages, api_url, model='ft:gpt-3.5-turbo-0613:personal:amc-mgnrega:98Wln5lE')
                
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


@blp.route("/")
def jim():
    return render_template('rag.html')

@blp.route('/trial')
def trial():
    return render_template('trial.html')

@blp.route("/response", methods=['POST'])
def jim_response():
    message = request.json.get('message')
    pinecone_index = 'mgnrega'
    # llm = OpenAI()
    embeddings = OpenAIEmbeddings()
    vectorstore = PC.from_existing_index(pinecone_index, embeddings) # get the pinecone embeddings
    retriever = vectorstore.as_retriever()
    prompt = ChatPromptTemplate(input_variables=['context', 'question'],
                                metadata={'lc_hub_owner': 'rlm', 'lc_hub_repo': 'rag-prompt', 'lc_hub_commit_hash': '50442af133e61576e74536c6556cefe1fac147cad032f4377b60c436e6cdcb6e'}, 
                                messages=[HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['context', 'question'], 
                                template="You are JiM, a waterbot. You are a watershed expert with experience in MGNREGA operations. \
                                    Use the following pieces of retrieved context to answer the question. Keep your tone professional and humble. \
                                    If you don't know the answer, just say 'I dont know. Please contact Mr. Krishan Tyagi, Project Manager, WASCA II \
                                    for any further clarification. I am still making a guess. Hope it helps!'. Then use your knowledge to make a guess. \
                                    Help the user to the best of your ability.\nQuestion: {question} \nContext: {context} \nAnswer:"))])
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )
    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    def generate():
        for chunk in rag_chain_with_source.stream(message):
            if 'answer' in chunk.keys():
                if chunk['answer']:
                    yield chunk['answer']
    return stream_with_context(generate())

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))