from iTraining.app import create_app

app = create_app()
app.debug = True

# @app.route('/')
# def hello_world():
#     return '<h1>Hello, World! I am iTraining.</h1> \
#         Please go visit <a href="/">Core App</a><br><a href="/iwater">iWater</a>'