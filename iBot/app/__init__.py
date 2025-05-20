import os
from flask import Flask
from flask_smorest import Api

from iBot.app.routes.chat import blp as chat
from iBot.app.routes.openai import blp as openai


def create_app():
    app = Flask(__name__)
    app.config['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
    app.config["OPENAI_API_URL"] = os.getenv("OPENAI_API_URL")
    app.config['SECRET_KEY']=os.getenv("WATERBOT_SECRET_KEY")

    # PINECONE
    app.config['PINECONE_API_KEY']=os.getenv("PINECONE_API_KEY")
    app.config['PINECONE_INDEX_HOST']=os.getenv("PINECONE_INDEX_HOST")
    from pinecone import Pinecone
    # initialize pinecone
    pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])

    # SWAGGER UI
    # app.config['API_TITLE']='iBot'
    # app.config['API_VERSION']='v1'
    # app.config["OPENAPI_VERSION"] = "3.0.3"
    # app.config["OPENAPI_URL_PREFIX"] = "/"
    # app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"   
    # app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # api = Api(app)

    # api.register_blueprint(chat, url_prefix='chat')
    app.register_blueprint(openai)
    return app
