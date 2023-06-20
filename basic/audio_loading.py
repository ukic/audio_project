from librosa import load
from pyaudio import PyAudio, paFloat32
from scipy.io.wavfile import write
from numpy import float32, frombuffer, concatenate
from threading import Thread, Event
from basic.track import Track


# Constant values
CHUNK = 1024
SAMPLE_RATE = 44100


def import_wav(path: str):
    audio, fs = load(path)
    return Track(audio, fs)


def export_wav(track: Track, path: str):
    write(path, track.fs, track.y.astype(float32))
    return 0


class AudioRecorder:
    def __init__(self):
        self.audio = []
        self.fs = SAMPLE_RATE
        self.event = None
        self.thread = None

    def record(self):
        self.audio = []
        recorder = PyAudio()
        stream = recorder.open(format=paFloat32, rate=SAMPLE_RATE, channels=2, frames_per_buffer=CHUNK, input=True)
        while not self.event.is_set():
            data = stream.read(CHUNK)
            self.audio = concatenate((self.audio, frombuffer(data, dtype=float32)), axis=0)
        stream.stop_stream()
        stream.close()
        recorder.terminate()

    def start_recording(self):
        self.event = Event()
        self.thread = Thread(target=self.record)
        self.thread.start()

    def stop_recording(self):
        self.event.set()
        self.thread.join()
        return Track(self.audio, SAMPLE_RATE)
