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
    peakFst = peakSec = secVal = None
    maxPeak = 0
    tresh = sorted(data.data)[round(data.size/2)] # Treshold for finding rising edge (median)
    margin = 100 # Margin when checking if value is under treshold
    
    for i, val in enumerate(data.data): # Get value and index from arr
        # Check if we are looking for the first or second index
        if not secVal:
            # If first index is empty set the index
            if val > maxPeak: 
                peakFst = i
                maxPeak = val
            # Check if the value has dropped below the threshold to indicate that we can find the second value
            elif val < tresh - margin and maxPeak > tresh:
                secVal = True
                maxPeak = 0
        # Find the second index
        elif val > maxPeak:
            peakSec = i
            maxPeak = val
    # Make sure both indexes are valid
    if peakFst != None and peakSec != None:
        # Calculate time between indexes. Time between samples is 1/freq s.
        # BPS is 2nd - 1st * time between samples.
        bpm = (int(peakSec) - int(peakFst)) * (1/freq) * 60
    else: bpm = 0
    
    return f'{bpm} BPM' if bpm < 240 and bpm > 30 else 'Bad data'#, [tresh, margin], [peakFst, peakSec]
        
while True:
    if sampls.full:
        print(calcBPM(sampls))
        
        # Debug
        #print(sampls.data)
        #print(f'max = {max(sampls.data)} min = {min(sampls.data)}')
        
        # Clear data for new samples
        sampls.clear()
    