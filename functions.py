import sys, os
import numpy as np
from scipy.io.wavfile import read,write
import winsound as ws
import math
import matplotlib.pyplot as plt

MAX_SIZE =32768 #zmienna określająca maksymalna wartośc w przetwarzaniu danych przy rozdzielczości danych 16-bitowych

# klasa obiektu z polami do przechowania:
#- tablicy dwukolumnowj danych
#- czestotliwosc probkowania
# oraz metod służących do przetwarzania dźwięku
class Functions(object):
	# konstruktor wczytujący ramkę danych i próbkowanie
	def __init__(self, path):
		self.fs, self.data = read(path)

	# zapis do pliku o podanej nazwie
	def save(self, output):
		write(str(output), self.fs, self.data)

	# odtwarza dane przechowane w polu klasy
	def play(self):
		tmp='tmp.wav'
		self.save(tmp)
		ws.PlaySound(tmp,ws.SND_ALIAS)
		os.remove(tmp)

	# rozdziela sygnał stereo na poszczegolne kanały
	def split_channels(self):
		ch1=self.data[:,0]
		ch2=self.data[:,1]
		return ch1,ch2

	# scala kanały w tablice stereo
	def merge_channels(self,ch1,ch2):
		merg=np.stack((ch1,ch2),axis=1)
		self.data=np.int16(merg)

	# nakłada na dźwięk echo po podanym czasie
	def echo(self,time):
		out_data= np.zeros(shape=(len(self.data),2))
		delay = time * self.fs

		if delay==0:
			return

		iter=0
		for i in self.data:
			out_data[iter,0] = i[0] + self.data[iter - int(delay),0]
			out_data[iter,1] = i[1] + self.data[iter - int(delay),1]
			iter+=1

		self.data=np.int16(out_data)

	# odtwarza dźwięk od tyłu
	def reverse(self):
		self.data=self.data[::-1]

	# zmiana głośności dźwięku wraz z zabezpieczeniem przed zniszczeniem próbek
	def volume(self,gain):
		out=np.zeros(shape=(len(self.data),2))
		max=MAX_SIZE

		for i in self.data:
			if abs(i[0])*gain > max:
				max=abs(i[0])*gain

		sk=MAX_SIZE/max
		iter=0
		for i in self.data:
			out[iter,0]=(gain*sk*i[0])
			out[iter,1]=(gain*sk*i[1])
			iter+=1
		self.data=np.int16(out)

	# zmiana prędkości odtwarzania
	def speed(self,gain):
		ntime = np.arange(0, len(self.data), gain)
		tmp=[]
		for i in ntime:
			if i < len(self.data):
				tmp.append(i)
		tmp=np.array(tmp).astype(int)
		self.data=self.data[tmp]

	# przycięcie utworu w podanych granicach
	def cut(self,start,stop):
		t2=round(stop*self.fs)
		t1=round(start*self.fs)
		roz=t2-t1
		out_data= np.zeros(shape=(roz,2))

		iter=0
		for i in range(t1,t2):
			out_data[iter,0] = self.data[i,0]
			out_data[iter,1] = self.data[i,1]
			iter+=1
		self.data=np.int16(out_data)

	# wizualizacja danych w postaci próbek dźwięku oraz jego widma
	def visual(self):
		t=np.arange(0,len(self.data)/self.fs,1/self.fs) #oś pozioma w sek
		fig,axes=plt.subplots(nrows=2, ncols=1, figsize=(10,4))
		axes[0].plot(t,self.data[:,0],label="L")
		axes[0].plot(t,self.data[:,1],label="P")
		axes[0].grid(axis='both')
		axes[0].legend()

		axes[1].magnitude_spectrum(self.data[:,0],Fs=self.fs,label="L")
		axes[1].magnitude_spectrum(self.data[:,1],Fs=self.fs,label="P")
		axes[1].grid(axis='both')
		axes[1].legend()
		plt.savefig("out_sound.jpg")

	# Oblicza poziom głośności ze średniej kwadratowej
	def true_rms(self):
		sqr1=0
		sqr2=0
		for i in range(len(self.data)):
			tmp1=int(self.data[i,0])
			tmp2=int(self.data[i,1])
			sqr1+=(tmp1**2)
			sqr2+=(tmp2**2)
		mean1=sqr1/(len(self.data))
		mean2=sqr2/(len(self.data))
		root1=math.sqrt(mean1)
		root2=math.sqrt(mean2)

		L=20*math.log((root1/MAX_SIZE),10)
		P=20*math.log((root2/MAX_SIZE),10)
		Ster=(L+P)/2

		return round(L,3),round(P,3),round(Ster,3)
