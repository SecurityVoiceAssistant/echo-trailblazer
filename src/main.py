from speech_recognition import transcribe

filename = 'https://cdn-media.huggingface.co/speech_samples/sample1.flac'
text = transcribe(filename)
print(text)

