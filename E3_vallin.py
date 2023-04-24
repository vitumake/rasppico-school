from piotimer import Piotimer
from machine import ADC
from clss import samplData

freq = 250
adc = ADC(26)
sampls = samplData(500)

def recSampl(penis):
    # Go in raw no filter
    sampls.put(adc.read_u16())

tmr = Piotimer(mode=Piotimer.PERIODIC, freq=freq, callback=recSampl)

def calcBPM(data):
    maxPeak = indxPeak = 0
    peaks = []
    tresh = sorted(data.data)[round(data.size/2)] # Treshold for finding rising edge (median)
    margin = 300 # Margin when checking if value is under treshold
    
    for i, val in enumerate(data.data): # Get value and index from arr
        # Check if we are looking for the first or second index
        if val > maxPeak:
            maxPeak = val
            indxPeak = i
        if val < tresh - margin and not indxPeak == 0 and not val == 0:
            peaks.append(indxPeak)
            indxPeak = maxPeak = 0
            
    # Make sure both indexes are valid
    if len(peaks) > 5:
        # Calculate time between indexes. Time between samples is 1/freq s.
        # BPS is 2nd - 1st * time between samples.
        bpmDelta = []
        for i in range(len(peaks)-1):
            bpmDelta.append((int(peaks[i+1]) - int(peaks[i])) * (1/freq) * 60)
        bpm = sum(peaks) / len(peaks)
    else: bpm = 0
    
    
    return f'{bpm} BPM' if bpm < 240 and bpm > 30 else 'Bad data', len(peaks)
        
while True:
    if sampls.full:
        print(calcBPM(sampls))
        
        # Debug
        #print(sampls.data)
        #print(f'max = {max(sampls.data)} min = {min(sampls.data)}')
        
        # Clear data for new samples
        sampls.clear()
    