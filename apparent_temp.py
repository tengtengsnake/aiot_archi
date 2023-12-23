def apparent_temp(real_temp, air_pressure):
    # 體感溫度=(1.04×溫度)+(0.2×水氣壓)—(0.65×風速)—2.7
    windspeed = 0
    return float((1.04 * float(real_temp)) + (0.2 * float(air_pressure)) - (0.65 * windspeed) - 2.7)
