from flask import Flask

app = Flask(__name__)
#from app import views

import disasterview.views

# if __name__ == '__main__':
#   app.run(debug=True)
