import pandas as pd
import numpy as np
# data = {}
# data['id'] = [1,2,3,4,5,6,7]
# data['Name'] = ['John','Mike','Sally','Jane','Joe','Dan','Phil']
# data['Salary'] = [300,200,550,500,600,600,550]
# data['manager_id'] = [3,3,4,7,7,3,'NULL']
# df = pd.DataFrame(data)  

#without using pandas dataframe 
#question 1a
id_ = [1,2,3,4,5,6,7]
Name = ['John','Mike','Sally','Jane','Joe','Dan','Phil']
Salary = [300,200,550,500,600,600,550]
manager_id = [3,3,4,7,7,3,'NULL']
higher_salary = []
for index,each in enumerate(id_):
    #data cleaning
    if type(manager_id[index]) != int:
        continue
    if Salary[manager_id[index]-1] < Salary[index]:
        higher_salary.append(Name[index])
print(higher_salary)
#output ['Sally', 'Joe', 'Dan']

#question 1b
not_managing = []
for index,each in enumerate(id_):
    if each not in manager_id:
        not_managing.append(index)
print(not_managing)
Salary_nm = []
Name_nm = []
for index in not_managing:
    Salary_nm.append(Salary[index])
    Name_nm.append(Name[index])

print(Name_nm)
print(np.average(Salary_nm))
#output 
#['John', 'Mike', 'Joe', 'Dan']
#425.0
