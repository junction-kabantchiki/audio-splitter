import glob
import os
import youtube_dl
from pydub import AudioSegment

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'wav',
      'preferredquality': '192',
    }],
    # 'outtmpl': 'target.wav',
    'outtmpl': '%(title)s.%(ext)s'
}


# brew install ffmpeg # sudo apt install ffmpeg

def split_wav_store(fname, window_size=5000, format='wav', splits_dir='splits'):

  def prepare_tmp_dir(path):
    if os.path.isdir(path):
      for f in os.listdir(path):
        os.remove(os.path.join(path, f))
    else:
      os.mkdir(path)

  def split_audio(fname, window_size, format, dir):
    files = []
    audio = AudioSegment.from_wav(fname)
    t1 = 0
    t2 = window_size
    idx = 0

    while t2 < len(audio):
      fname = f'{splits_dir}/{idx}.wav'
      files.append(fname)

      audio[t1:t2].export(out_f=fname, format=format, bitrate='48k')
      t1 = t2
      t2 = t1 + window_size
      idx += 1

    return files

  prepare_tmp_dir(splits_dir)
  return split_audio(fname, window_size, format, splits_dir)


def download_wav(youtube_link):
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([youtube_link])

def get_latest_upload(folder='.'):
  files = glob.glob(os.path.join(folder, '*.wav'))
  files.sort(key=lambda x: os.path.getmtime(x))
  return files[-1]

def download_split(link):
  download_wav(link)
  file = get_latest_upload()
  splitted_files = split_wav_store(file)
  return splitted_files

def infer(files):
  pass

def main():
  splits = download_split('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
  results = infer(splits)

if __name__ == '__main__':
  main()
