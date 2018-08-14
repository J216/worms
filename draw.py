from random import randrange, choice
from math import sin, cos, radians

import gimp
from gimp import pdb

# execfile('/home/amber/scripts/draw.py')
# draw a single brush point
def draw_line(x1, y1, x2, y2):
    image = gimp.image_list()[0]
    drawable = pdb.gimp_image_active_drawable(image)
    ctrlPoints = (x1, y1, x2, y2)
    pdb.gimp_paintbrush_default(drawable, len(ctrlPoints), ctrlPoints)
    return ctrlPoints

def brush_size(size=-1):
    image = gimp.image_list()[0]
    drawable = pdb.gimp_image_active_drawable(image)
    if size < 1:
        size = randrange(2, ((image.height + image.width) / 8))
    pdb.gimp_context_set_brush_size(size)
                                            
# Set brush opacity
def brush_opacity(op=-1):
    if op == -1:
        op = randrange(15, 100)
    pdb.gimp_brushes_set_opacity(op)
    return op

# Set random brush color no parameters set random
def brush_color(r1=-1, g1=-1, b1=-1, r2=-1, g2=-1, b2=-1):
    if not r1 == -1:
        pdb.gimp_context_set_foreground((r1, g1, b1))
    if not r2 == -1:
        pdb.gimp_context_set_background((r2, g2, b2))
    elif r1 == -1:
        r1 = randrange(0, 255)
        g1 = randrange(0, 255)
        b1 = randrange(0, 255)
        r2 = randrange(0, 255)
        g2 = randrange(0, 255)
        b2 = randrange(0, 255)
        pdb.gimp_context_set_foreground((r1, g1, b1))
        pdb.gimp_context_set_background((r2, g2, b2))
    return (r1, g1, b1, r2, g2, b2)

def brush_mode(mode=-1):
    if mode == -1:
        mode = randrange(25)
    pdb.gimp_context_set_paint_mode(mode)
    
def add_layer(opacity=100,mode=0):
    image = gimp.image_list()[0]
    new_layer = gimp.Layer(image, "worms", image.width, image.height, 0, opacity, mode)
    pdb.gimp_image_add_layer(image, new_layer, 0)
    pdb.gimp_image_set_active_layer(image, new_layer)
    drawable = pdb.gimp_image_active_drawable(image)

# update active image sets global var to current draw area, can't set image to active as of now...
def update_image():
    pdb.gimp_displays_flush()

def turn_ant(ant_in, heading=-1):
    if heading == -1:
        heading = randrange(-15,15)
    ant_in['heading'] += heading
    if ant_in['heading'] > 360:
        ant_in['heading'] == 0
    if ant_in['heading'] < 0:
        ant_in['heading'] == 360
    return ant_in

def turn_ants(ants_in):
    turned_ants = []
    for ant in ants_in:
        turned_ants.append(turn_ant(ant))
    return turned_ants

def move_ant(ant_in, distance=45):
    ctrlpoints = []
    image = gimp.image_list()[0]
    ctrlpoints.append(ant_in['x'])
    ctrlpoints.append(ant_in['y'])
    ant_in['x'] += int(round(sin(radians(ant_in['heading']))*distance))
    if ant_in['x'] < 0:
        ant_in['x'] = image.width
    if ant_in['x'] > image.width:
        ant_in['x'] = 0
    ant_in['y'] += int(round(cos(radians(ant_in['heading']))*distance))
    if ant_in['y'] < 0:
        ant_in['y'] = image.height
    if ant_in['y'] > image.height:
        ant_in['y'] = 0
    ctrlpoints.append(ant_in['x'])
    ctrlpoints.append(ant_in['y'])
    if abs(ctrlpoints[0] - ctrlpoints[2])> image.width/2 or abs(ctrlpoints[1] - ctrlpoints[3])> image.height/2:
        draw_line(ctrlpoints[0],ctrlpoints[1],ctrlpoints[0],ctrlpoints[1])
    else:
        draw_line(*ctrlpoints)
    return (ant_in, ctrlpoints)

def move_ants(ants_in):
    moved_ants = []
    for ant in ants_in:
        moved_ants.append(move_ant(ant)[0])
    return moved_ants


ant0 = {'id':0, 'x':0, 'y':0, 'heading':190}
ant1 = {'id':1, 'x':0, 'y':5, 'heading':130}
ant2 = {'id':2, 'x':5, 'y':0, 'heading':115}
ants=[ant0,ant1,ant2]
size = 10
count = 0
while 1:
    count += 1
    if count%633 == 0:
        add_layer(mode=6)
    if count%333 == 0:
        brush_mode()
    if count%100 == 0:
        brush_color()
    size += randrange(-7,7)
    if size < 3:
        size = 5
    if size > 75:
        size = 69
    pdb.gimp_context_set_brush_size(size)
    ant=turn_ants(ants)
    ants=move_ants(ants)
    if count%5 == 0:
        update_image()
