
def read(filename):
    values = []
    with open(filename, 'r') as f:
        for line in f:
            l = line.split()
            for e in l:
                try: int(e)
                except: e = ''
                values.append(e)

    return {'values': values, 'size':9}
