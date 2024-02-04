import os
from vosk import Model, KaldiRecognizer
import pyaudio


#Download model from here
# https://github.com/alphacep/vosk-space/blob/master/models.md

model_path = 'vosk-model-small-en-us-0.15\\vosk-model-small-en-us-0.15'
if not os.path.exists(model_path):
    print("Please download a model and specify the correct path.")
    exit(1)

model = Model(model_path)

mic_index = None

rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, input_device_index=mic_index, frames_per_buffer=8192)
stream.start_stream()

print("Recording started, speak into the microphone...")

while True:
    data = stream.read(4096, exception_on_overflow=False)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        print(result)
    else:
        partial = rec.PartialResult()
        print(partial)

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
