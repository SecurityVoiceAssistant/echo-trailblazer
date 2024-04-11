from speech_recognition import pipe
# from speech_recognition import prompt

filename = 'https://cdn-media.huggingface.co/speech_samples/sample2.flac'

sr_result = pipe(filename)['text']
print(sr_result)

# answer = prompt(sr_result)
# print(answer)
