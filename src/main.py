from speech_recognition import pipe
# from speech_recognition import prompt

filename = 'https://cdn-media.huggingface.co/speech_samples/sample1.flac'

result = pipe(filename, generate_kwargs={"task": "translate"})
text = result['text']
print(text)

# answer = prompt(text)
# print(answer)

