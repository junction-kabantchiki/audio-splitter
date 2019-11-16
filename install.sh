git clone https://github.com/x4nth055/emotion-recognition-using-speech model/
pip install -r model/requirements.txt
pip install -r splitter/requirements.txt
ENV PYTHONPATH "${PYTONPATH}:/app/model"
ENV PYTHONPATH "${PYTONPATH}:/app/splitter"
