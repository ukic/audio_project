from numpy import ndarray


def transcribe(audio: ndarray, model):
    return model.transcribe(audio=audio)["text"]
