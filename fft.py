from scipy.io.wavfile import read
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt

# Input:        inputSignal:    Eingangssignal
#               nDeleteFreq:    Anzahl der zu löschenden Frequenzen
#               fftLength:      Länge der FFT
#
# Output:       outputSignal:   Ausgangssignal
#
# Nützliche Befehle/Collections/Libs: numpy, ftt, scipy.io.wavfile,...

def fft(inputSignal,nDeleteFreq,fftLength):
    outputSignal = np.empty(0, dtype = np.int16)


    for x in range(0,len(inputSignal),fftLength): # Die verschiedenen Segmente
        if x + fftLength >  len(inputSignal):
            upperBound = len(inputSignal)
        else:
            upperBound = x + fftLength

        #plt.plot(inputSignal[x:upperBound])
        #plt.show()

        fftSeg = np.fft.fft(inputSignal[x:upperBound])
        #plt.plot(np.abs(fftSeg[:int(fftLength/2)]))

        fftSeqChanged = np.copy(fftSeg)#wegen dem graph mit copie arbeiten

        absolut = np.abs(fftSeqChanged[:int(fftLength / 2)])  # das fft-array in absolute werte ändern

        for x in range(0,nDeleteFreq,1):
            lowestIndex = np.argmin(absolut) # index mit niedrigster amplitude
            absolut[lowestIndex] =  100000 #auf hohen wert setzten, damit nicht immer der selbe genommen wird
            fftSeqChanged[lowestIndex] = 0

        #plt.plot(np.abs(fftSeqChanged[:int(fftLength / 2)]))
        #plt.show()

        newSig = np.empty(0, dtype=int)
        newSig = np.concatenate((newSig, fftSeqChanged[0:int(fftLength / 2)]), axis=None)
        reversed_arr = fftSeqChanged[::-1]
        newSig = np.concatenate((newSig, reversed_arr[0:int(fftLength / 2)]), axis=None)

        wav =  np.fft.ifft(newSig)
        outputSignal = np.concatenate((outputSignal,wav), axis=None)

        #plt.plot(outputSignal)
        #plt.show()

    return outputSignal

def main():
    samplerate, wavData = read("ceremony.wav")
    #plt.plot(wavData)
    #plt.show()

    #fftTest = np.fft.fft(wavData)
    #test = np.fft.ifft(fftTest)

    output = fft(wavData,50,1000)
    real = np.real(output)
    write("Test.wav",samplerate,real.astype(np.int16))


    #plt.plot(wavData)
    #plt.plot((output))
    #plt.show()

if __name__ == "__main__":
    main()
