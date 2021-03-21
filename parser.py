from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         translate: create a translation matrix,
                    then multiply the transform matrix by the translation matrix -
                    takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge matrix
         display: clear the screen, then
                  draw the lines of the edge matrix to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge matrix to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing
See the file script for an example of the file format
"""


def parse_file(fname, points, transform, screen, color):
    f = open(fname, 'r')
    script = []
    for x in f:
        x = x.rstrip()
        script.append(x)
    f.close()
    i = 0
    while i < len(script):
        if script[i] == 'line' or script[i] == 'scale' or script[i] == 'translate' \
                or script[i] == 'move' or script[i] == 'rotate':
            i += 1
            if script[i-1] == 'rotate':
                num = (script[i])
                num = int(num[2:])
                if 'x' in script[i]:
                    r = make_rotX(num)
                elif 'y' in script[i]:
                    r = make_rotY(num)
                else:
                    r = make_rotZ(num)
                matrix_mult(r, transform)
            else:
                num = [int(x) for x in script[i].split()]
                if script[i-1] == 'line':
                    add_edge(points, num[0], num[1], num[2], num[3], num[4], num[5])
                elif script[i-1] == 'scale':
                    s = make_scale(num[0], num[1], num[2])
                    matrix_mult(s, transform)
                elif script[i-1] == 'translate' or 'move':
                    t = make_translate(num[0], num[1], num[2])
                    matrix_mult(t, transform)
        elif script[i] == 'ident':
            ident(transform)
        elif script[i] == 'apply':
            matrix_mult(transform, points)
            for r in range(len(points[0])):
                for c in range(len(points)):
                    points[c][r] = int(points[c][r])
        elif script[i] == 'display':
            clear_screen(screen)
            draw_lines(points, screen, color)
            display(screen)
        elif script[i] == 'save':
            i += 1
            clear_screen(screen)
            draw_lines(points, screen, color)
            save_extension(screen, script[i])
        elif script[i] == 'quit':
            print('Quitting')
            break
        else:
            pass
        i += 1
