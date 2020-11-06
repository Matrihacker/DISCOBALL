import array
import math
import audiobusio
import board
import neopixel
import time
import ulab
import ulab.extras
import ulab.vector
from random import randint

# Number of total pixels - 10 build into Circuit Playground
pixels=neopixel.NeoPixel(board.NEOPIXEL,10,auto_write=False,brightness=1)

#adjusting the threshold of the light ,default 43
kiraThreshold=38

#Offset the hue  of the neopixel
offsetHue=240


# Sizr of FFT range
fft_size = 32


def mean(values):
    return sum(values) / len(values)



def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r=r/100
    g=g/100
    b=b/100
    r, g, b = int(r * 255), int(g * 255), int(b * 255)

    return r, g, b




def colorAss(data):


    for i in range(0,10):
        hue=offsetHue+i*36
        if hue>360:
            hue-=360
        elif hue<0:
            hue=360-hue

        if data[i]>=kiraThreshold:
            pixels[i]=hsv2rgb(hue, 100, 100)

        else:
            pixels[i]=hsv2rgb(0, 0, 0)

    pixels.show()





# Main program
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,sample_rate=16000, bit_depth=16)

# Record an initial sample to calibrate. Assume it's quiet when we start.
samples = array.array('H', [0] * (fft_size+3))
mic.record(samples, len(samples))


while True:
    max_all = 10
    mic.record(samples, len(samples))
    samplesfft= ulab.array(samples[3:])
    spectrogram1 = ulab.extras.spectrogram(samplesfft)
    spectrogram1 = ulab.vector.log(spectrogram1 + 1e-7)
    spectrogram1 = spectrogram1[1:(fft_size//2)-1]
    min_curr = ulab.numerical.min(spectrogram1)
    max_curr = ulab.numerical.max(spectrogram1)

    if max_curr > max_all:
        max_all = max_curr
    else:
        max_curr = max_curr-1

    min_curr = max(min_curr, 3)
    data = (spectrogram1 - min_curr) * (51. / (max_all - min_curr))
    colorAss(data)

