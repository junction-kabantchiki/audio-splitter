from flask import Flask, request
import splitter.split as split
from model.deep_emotion_recognition import DeepEmotionRecognizer

app = Flask(__name__)


def prepare_model():
  deeprec = DeepEmotionRecognizer(emotions=['angry', 'sad', 'neutral', 'ps', 'happy'],
                                  n_rnn_layers=2,
                                  n_dense_layers=2,
                                  rnn_units=128,
                                  dense_units=128)
  deeprec.train()
  print(deeprec.test_score())
  # print(f"Prediction: {prediction}")
  return deeprec


deeprec = prepare_model()

@app.route('/getmood')
def download_predict():
  youtube_id = request.args['id']
  window_size = request.args.get('window', 5000)
  files = split.download_split(youtube_id, window=window_size)
  predictions = [deeprec.predict_proba(f) for f in files]
  # prediction = deeprec.predict('data/validation/Actor_10/03-02-05-02-02-02-10_angry.wav')


  return {'files': files}, 200


if __name__ == '__main__':
  app.run(host='0.0.0.0')