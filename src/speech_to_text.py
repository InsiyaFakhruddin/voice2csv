import speech_recognition as sr

import speech_recognition as sr

recognizer = sr.Recognizer()
audio_data = []

def callback(recognizer, audio):

    global audio_data
    audio_data.append(audio)

def start_background_recording():
    global audio_data
    audio_data = []
    mic = sr.Microphone()
    stop_fn = recognizer.listen_in_background(mic, callback)
    return stop_fn

def transcribe_all():
    global audio_data
    if not audio_data:
        return "[No audio was recorded]"

    try:
        # Merge all audio chunks
        full_audio = sr.AudioData(
            b''.join([a.get_raw_data() for a in audio_data]),
            audio_data[0].sample_rate,
            audio_data[0].sample_width
        )
        text = recognizer.recognize_google(full_audio)
        return text
    except sr.UnknownValueError:
        return "[Could not understand audio]"
    except sr.RequestError:
        return "[Error connecting to speech recognition service]"
    except Exception as e:
        return f"[Unexpected error: {e}]"


def record_and_transcribe(timeout=60, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Listening... Speak now.")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "[Could not understand audio]"
    except sr.RequestError:
        return "[Error connecting to speech recognition service]"
