from piotimer import Piotimer
from machine import ADC
from clss import samplData

freq = 250
adc = ADC(26)
sampls = samplData(500)

def recSampl(penis):
    sampls.put(adc.read_u16())

tmr = Piotimer(mode=Piotimer.PERIODIC, freq=freq, callback=recSampl)

def calcBPM(data):
    secRising = False
    risngFst = None
    risgnSec = None
    tresh = 1000 # Treshold for finging rising edge
    margin = 500 # Margin when checking if value is under treshold
    
    for i, val in enumerate(data.data): # Get value and index from arr
        # Check if we are looking for the first or second index
        if not secRising:
            # If first index is empty set the index
            if val > data.average() + tresh and risngFst == None: 
                risngFst = i
            # Check if the value has dropped below the threshold to indicate that we can find the second value
            elif val < data.average() + tresh - margin and risngFst != None:
                secRising = True
        # Find the second index
        elif val > data.average() + tresh:
            risgnSec = i
    # Make sure both indexes are valid
    if risngFst != None and risgnSec != None:
        # Calculate time between indexes. Time between samples is 1/freq s.
        # BPS is 2nd - 1st * time between samples.
        bpm = f'{(int(risgnSec) - int(risngFst)) * 1/freq * 60} BPM'
    else: bpm = 'Bad data'
    
    return bpm 
        
while True:
    if sampls.full:
        print(calcBPM(sampls))
        # Clear data for new samples
        sampls.clear()
    