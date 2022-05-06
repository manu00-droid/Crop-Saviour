from gtts import gTTS


def text_to_speech(text, file_name):
    tts = gTTS(text)
    tts.save(f"{file_name}.mp3")

# text = "Hello! My name is Bharath."
# tts = gTTS(text)
# tts.save("hi.mp3")
