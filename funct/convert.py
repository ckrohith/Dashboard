#!/usr/bin/env python3

def convert_bytes(byte):
    if byte < 1024:
        if byte == 1:
            return " ".join((str(byte), "byte"))

        else:
            return " ".join((str(byte), "bytes"))

    elif 1024 <= byte < 1024**2:
        return " ".join((str(round(byte/1024, 2)), "KB"))

    elif 1024**2 <= byte < 1024**3:
        return " ".join((str(round(byte/(1024**2), 2)), "MB"))

    elif 1024**3 <= byte < 1024**4:
        return " ".join((str(round(byte/(1024**3), 2)), "GB"))

    else:
        return " ".join((str(round(byte/(1024**4), 2)), "TB"))

def convert_seconds(seconds):
    days = seconds // 86400
    hours = (seconds - (days * 86400)) // 3600
    minutes = (seconds - (days * 86400) - (hours * 3600)) // 60

    if days == 0:
        days = ""

    elif days == 1:
        days = "".join((str(int(days)), " day "))

    else:
        days = "".join((str(int(days)), " days "))

    if hours == 1:
        hours = "".join((str(int(hours)), " hr "))

    else:
        hours = "".join((str(int(hours)), " hrs "))

    return ("".join((days, hours, str(int(minutes)), " min")))

def convert_frequency(freq):
    if freq < 1000:
        return "".join((str(round(freq, 2)), " MHz"))

    else:
        return "".join((str(round(freq/1000, 2)), " GHz"))