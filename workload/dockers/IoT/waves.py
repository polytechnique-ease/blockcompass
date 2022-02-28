import wave
import __main__ as Simulator

def load_wave():
    waveFile = wave.open('asd.wav', 'rb')
    params = waveFile.getparams()
    # params:  (2, 2, 48000, 2880000, 'NONE', 'not compressed')
    rate = float(params[2])
    frames = waveFile.getnframes()
    # number of frames aggregated in each timestamp
    splPerTs = rate / 120
    asdWrapLimit = int(params[3] / splPerTs)
    for i in range(0, asdWrapLimit):
        data = waveFile.readframes(int(splPerTs))
        Simulator.wave_data.append(data)
    Simulator.L.info("Wave data: %d flames" % len(Simulator.wave_data))