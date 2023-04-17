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
    rising = False
    risngFst = None
    risgnSec = None
    tresh = 1000 # Treshold for finging rising edge
    margin = 500
    
    for i, val in enumerate(data.data):
        if not rising:
            if val > data.average() + tresh and risngFst == None:
                risngFst = i
            elif val < data.average() + tresh - margin and risngFst != None:
                rising = True
        elif val > data.average() + tresh:
            risgnSec = i
    
    if risngFst != None and risgnSec != None:
        bpm = f'{(int(risgnSec) - int(risngFst)) * 1/freq * 60} BPM'
    else: bpm = 'Bad data'
    
    return bpm 
        
while True:
    if sampls.full:
        print(calcBPM(sampls))
        sampls.clear()
    