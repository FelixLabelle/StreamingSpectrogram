import pyaudio
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
import numpy as np

CHUNK = 1024
CHANNELS = 1
SAMPLING_FREQ = 10000

# TODO: fix delay that accumulates
# https://matplotlib.org/api/animation_api.html#module-matplotlib.animation
# TODO: figure out how to kill stream when windows closes
try:
	print("Starting stream")
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16,
					channels=CHANNELS,
					rate=SAMPLING_FREQ,
					input=True,
					frames_per_buffer=CHUNK)

	print("The frequential resolution is ", (2*CHUNK/SAMPLING_FREQ), " Hz per bin")
	# Should I increase the chunk size?
	# Is putting the last data worth it?
	plt.ion()
	prevData = np.zeros(CHUNK, dtype=np.int16)
	while True:
		byteStream = stream.read(CHUNK)  #read audio stream
		data = np.frombuffer(byteStream, dtype=np.int16)
		f, t, Sxx = spectrogram(np.append(prevData,data), fs=SAMPLING_FREQ)
		prevData = data
		plt.pcolormesh(t, f, Sxx)
		plt.ylabel('Frequency [Hz]')
		plt.xlabel('Time [sec]')
		plt.show(block=False)
		plt.pause((CHUNK/SAMPLING_FREQ) * 0.5)

finally:
	plt.close()
	stream.stop_stream()
	stream.close()
	p.terminate()