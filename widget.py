#!/usr/bin/env python3

from math import pi

negative, notice, positive = (234/255, 56/255, 41/255), (246/255, 133/255, 17/255), (0, 143/255, 93/255)

def progress_bar(area, c, w, h, val, reverse=False):
    if reverse == False:
        if val < 60:
            color = positive

        elif 60 <= val < 90:
            color = notice

        else:
            color = negative

    elif reverse == True:
        if val > 40:
            color = positive

        elif 40 <= val < 10:
            color = notice

        else:
            color = negative

    c.set_line_width(h)
    c.set_source_rgb(230/255, 230/255, 230/255)
    c.move_to(0, h/2)
    c.line_to(w, h/2)
    c.stroke()

    c.set_line_width(h)
    c.set_source_rgb(color[0], color[1], color[2])
    c.move_to(0, h/2)
    c.line_to(w*val/100, h/2)
    c.stroke()

def circular_progress_bar(area, c, w, h, val):
    if val < 60:
        color = positive

    elif 60 <= val < 90:
        color = notice

    else:
        color = negative

    angle = (val*pi/50)-(0.5*pi)
    stroke = 5
    c.arc(w/2, w/2, (w-stroke)/2, 0, 2*pi)
    c.set_source_rgb(230/255, 230/255, 230/255)
    c.set_line_width(stroke)
    c.stroke()

    c.arc(w/2, w/2, (w-stroke)/2, -0.5*pi, angle)
    c.set_source_rgb(color[0], color[1], color[2])
    c.set_line_width(stroke)
    c.stroke()

    c.set_source_rgb(34/255, 34/255, 34/255)
    c.set_font_size(17)
    text = "".join((str(val), "%"))
    width = c.text_extents(text)[2]
    height = c.text_extents(text)[3]
    c.move_to((w/2)-(width/2), (w/2)+(height/2))
    c.show_text(text)