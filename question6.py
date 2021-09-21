with open('requirements.txt', 'r') as f:
    newlines = [line.rstrip() for line in f]
    for line in newlines:
        if '/' in line:
            print('possible date')
