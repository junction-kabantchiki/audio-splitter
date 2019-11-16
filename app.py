from flask import Flask, request
import splitter.split as split

app = Flask(__name__)


@app.route('/')
def hello_world():
  return 'Hello World!'

@app.route('/getmood')
def download_predict():
  youtube_id = request.args['id']
  files = split.download_split(youtube_id)

  return {'files': files}, 200


if __name__ == '__main__':
  app.run()
