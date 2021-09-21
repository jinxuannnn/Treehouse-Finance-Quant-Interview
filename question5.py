import os
#question 5a

#change '../TreehouseFinance' to 'my-python-project'
file_count = sum(len(files) for _, _, files in os.walk(r'../TreehouseFinance'))
print(file_count)
#output will be the number of python files in folder

#question 5b and c
lines = 0
header = True
begin_start = None
#Change '.' to '/my-python-project' , I used '.' for illustration
start = r'.'

def countlines(start, lines=0, header=True, begin_start=None):
    total_emptyline = 0
    total_commentoutline = 0
    total_linewithcode = 0
    total_function = 0
    if header:
        print('{:>10} |{:>10} | {:>10} |{:>12} | {:<10}'.format('emptylines', 'comment', 'coded lines','functions', 'file'))
        print('{:->11}|{:->11}|{:->13}|{:->13}|{:->6}'.format('', '', '','',''))

    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isfile(thing):
            if thing.endswith('.py'):
                emptyline = 0
                commentoutline = 0
                linewithcode = 0
                function = 0
                with open(thing, 'r') as f:
                    #making every line into a list
                    newlines = [line.rstrip() for line in f]
                    for line in newlines:
                        #empty line
                        if line == '':
                            emptyline += 1
                        #commented out line
                        elif line[0] == '#':
                            commentoutline +=1
                        #check if it is a commentted out line with spacing in front or line with code
                        elif line[0] == ' ':
                            tracker = 0
                            while True:
                                tracker += 1
                                if line[tracker] == ' ':
                                    continue
                                elif line[tracker] == '#':
                                    commentoutline += 1
                                    break
                                #check for function
                                elif line[tracker]+line[tracker+1]+line[tracker+2] == 'def':
                                    linewithcode += 1
                                    function += 1
                                    break
                                else:
                                    linewithcode += 1
                                    break
                        #check for function
                        elif line[0]+line[1]+line[2] == 'def':
                            linewithcode += 1
                            function += 1
                        else:
                            linewithcode += 1
                    #adding empty, comment and coded lines to total
                    total_emptyline += emptyline
                    total_commentoutline += commentoutline
                    total_linewithcode += linewithcode
                    total_function += function
                    if begin_start is not None:
                        reldir_of_thing = '.' + thing.replace(begin_start, '')
                    else:
                        reldir_of_thing = '.' + thing.replace(start, '')
                    #printing out the number of empty, commented out, coded lines and functions along with the corresponding file name
                    print('{:>10} |{:>10} | {:<11} |{:<12} |{:<20}'.format(
                            emptyline, commentoutline, linewithcode,function,reldir_of_thing))

    #recursive
    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isdir(thing):
            lines = countlines(thing, lines, header=False, begin_start=start)
    return total_emptyline, total_commentoutline, total_linewithcode , total_function

total_emptyline, total_commentoutline, total_linewithcode, total_function = countlines(start, lines=0, header=True, begin_start=None)
print(f'''Total empty lines: {total_emptyline}
Total commented out lines: {total_commentoutline}
Total lines with code: {total_linewithcode}
Total functions: {total_function}''')

#output
# emptylines |   comment | coded lines |   functions | file
# -----------|-----------|-------------|-------------|------
#          3 |        10 | 25          |0            |./question1py
#          1 |         0 | 11          |1            |./question2py
#          6 |         2 | 19          |1            |./question3py
#         21 |        39 | 73          |3            |./question4py
#          5 |        13 | 71          |1            |./question5py
# Total empty lines: 36
# Total commented out lines: 64
# Total lines with code: 199
# Total functions: 6
