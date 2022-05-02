from gtts import gTTS


def text_to_speech(text, language, file_name):
    speech = gTTS(text, lang=language)
    speech.save(f"{file_name}.mp3")
