from flask import Flask, request
from flask_cors import CORS
import splitter.split as split
import tensorflow as tf
from model.deep_emotion_recognition import DeepEmotionRecognizer

app = Flask(__name__)
cors = CORS(app)
graph = tf.Graph()

def prepare_model():

  with graph.as_default():
    deeprec = DeepEmotionRecognizer(emotions=['angry', 'sad', 'neutral', 'ps', 'happy'],
                                    n_rnn_layers=2,
                                    n_dense_layers=2,
                                    rnn_units=128,
                                    dense_units=128,
                                    )
    with graph.as_default():
        model_name = "model/results/" + deeprec.model_name
        deeprec.create_model()
        deeprec.model.load_weights(model_name)
        deeprec.model_trained = True

        print(deeprec.model_name)
    return deeprec


deeprec = prepare_model()

@app.route('/getmood')
def download_predict():
  youtube_id = request.args['id']
  window_size = request.args.get('window', 5000)
  files = split.download_split(youtube_id, window_size=window_size)
  with graph.as_default():
    predictions = [deeprec.predict_proba(f) for f in files]
  # prediction = deeprec.predict('data/validation/Actor_10/03-02-05-02-02-02-10_angry.wav')

  return {'predictions': predictions}, 200


if __name__ == '__main__':
  app.run(host='0.0.0.0')
