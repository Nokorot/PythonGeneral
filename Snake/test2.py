
import numpy

def old(from_color, to_color, height, width):
    channels = []
    for channel in range(3):
        from_value, to_value = from_color[channel], to_color[channel]
        channels.append(
            numpy.tile(
                numpy.linspace(from_value, to_value, width), [height, 1],
            ),
        )
    return numpy.dstack(channels)


def generate_gradient(from_color, to_color, height, width):
    channels = []
    for channel in range(3):
        from_value, to_value = from_color[channel], to_color[channel]
        channels.append(
            numpy.add.outer(
                numpy.linspace(0, 127, height), numpy.linspace(0, 127, width)
            )
        )
    return numpy.dstack(channels)

print old((0, 0, 0), (255, 255, 255), 3, 5)

gradient = generate_gradient((0, 0, 0), (255, 255, 255), 3, 5)
print gradient

'''

print numpy.tile( numpy.linspace(0, 1, 5), (5, 1) )

print numpy.add.outer(numpy.linspace(0, .5, 5), numpy.linspace(0, .5, 5))
'''
