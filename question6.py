import re
numberofdates = 0
with open('question6dates.txt', 'r') as f:
    #making each line into a list, the following check does not include 6d criteria
    newlines = [line.rstrip() for line in f]
    for line in newlines:
        numberofchars = len(line)
        char10 = []
        #loop through each char in the line until numberofchars-9 as a date is 10 chars long
        for i in range(numberofchars-9):
            year = 0
            month = 0
            day = 0
            x = re.findall("/", line[i:i+10])
            #check if there is two '/' in that 10 chars
            if len(x) == 2:
                y = re.findall("[0123456789]", line[i:i+10])
                #ensure that there is 8 digits in that 10 chars
                if len(y) == 8:
                    print(line[i:i+10])
                    #splitting string at '/'
                    z =  re.split("/", line[i:i+10])
                    for each in z:
                        #checking for year
                        if len(each) == 4:
                            if int(each) < 2022:
#                                 print('year verified')
                                year += 1
                        #checking for day and month
                        elif len(each) == 2:
                            if int(each) <= 12:
#                                 print('month verified')
                                month += 1
                            elif int(each) <= 31:
#                                 print('day verified')
                                day += 1
            if year == 1 and month == 1 and day == 1 or year == 1 and month == 2 and day == 0:
                print('date found')
                numberofdates += 1
print(f'Total dates found in this file is: {numberofdates}')
#output
# 22/09/2021
# date found
# 2021/03/31
# date found
# 2030/24/21
# 32/11/2020
# 31/31/2111
# 11/11/2020
# date found
# 11/31/2002
# date found
# 2030/24/21
# 20/11/2021
# date found
# Total dates found in this file is: 5
