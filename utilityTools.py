
def timeFixer(ms):
    if ms < 7200000:
        ms=ms/60000
        return f'{round(ms,1)}  Minutes'
    elif ms > 7200000:
        ms=ms/3600000
        return f'{round(ms)}  Hours'