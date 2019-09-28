import pyaudio
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
import numpy as np
import argparse


def handle_close(evt):
	raise KeyboardInterrupt 

def streamSpectrogram(CHUNK,SAMPLING_FREQ,CLOCK_IMPRECISION_FACTOR):
	try:
		print("Starting stream")
		p = pyaudio.PyAudio()
		stream = p.open(format=pyaudio.paInt16,
						channels=1,
						rate=SAMPLING_FREQ,
						input=True,
						frames_per_buffer=CHUNK)

		print("The frequential resolution is ", (2*CHUNK/SAMPLING_FREQ), " Hz per bin")
		# Should I increase the chunk size?
		# Is putting the last data worth it?
		plt.ion()
		fig = plt.figure()
		fig.canvas.mpl_connect('close_event', handle_close)
		prevData = np.zeros(CHUNK, dtype=np.int16)
		while True:
			byteStream = stream.read(CHUNK)  #read audio stream
			data = np.frombuffer(byteStream, dtype=np.int16)
			f, t, Sxx = spectrogram(np.append(prevData,data), fs=SAMPLING_FREQ)
			prevData = data
			plt.pcolormesh(t, f, Sxx)
			plt.ylabel('Frequency [Hz]')
			plt.xlabel('Time [sec]')
			plt.pause((CHUNK/SAMPLING_FREQ) * CLOCK_IMPRECISION_FACTOR)

	finally:
		plt.close()
		stream.stop_stream()
		stream.close()
		p.terminate()
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--chunk', type=int, default = 1024, help='Frame size(Power of 2)')
	parser.add_argument('--fs', type=int, default = 10000, help='Sampling frequency, determines frequency of the graph')
	parser.add_argument('--clockFactor', default = 0.5, help='Factor to help compensate for timing issues (lower = faster)')
	args = parser.parse_args()
	streamSpectrogram(args.chunk,args.fs,args.clockFactor)