import requests, json
import csv

#employee class that stores most of the data needed for the final csv (total enrolled will be calculated during the end)
class Employee:
    def __init__(self, employer, employee, spouses_enrolled, children_enrolled):
        self.employer = employer
        self.employee = employee
        self.spouses_enrolled = spouses_enrolled
        self.children_enrolled = children_enrolled
        #+1 due to the employee themselves being enrolled in the plan
        self.total_enrolled = spouses_enrolled + children_enrolled + 1

#gets the json from the url
url = requests.get("https://raw.githubusercontent.com/iagtech/challenges-data/main/coding-problem.json")
text = url.text
data = json.loads(text)

#json {'employer': 1, 'employee': 'John Adams', 'product': 'MEDICAL', 'is_enrolled': True, 'spouses_enrolled': 2, 'children_enrolled': 61}

#the map key is the combination of the employer and the employee, the value is the employee object
employeemap = {}

numemployers = 0
for x in data:
    if x['employer'] > numemployers:
        numemployers = x['employer']
    #updates the max employers for later iteration if the current employer is greater
    #if the employee is enrolled
    if x['is_enrolled']:
        #if the employee already exists in the map adds the current enrollments to the current employee
        if(str(x['employer'])+x['employee'] in employeemap):
            employeemap[str(x['employer'])+x['employee']].spouses_enrolled += x['spouses_enrolled']
            employeemap[str(x['employer'])+x['employee']].children_enrolled += x['children_enrolled']
            employeemap[str(x['employer'])+x['employee']].total_enrolled += x['children_enrolled'] + x['spouses_enrolled']
        #otherwise creates a new entry with the employee
        else:
            newemployee = Employee(x['employer'], x['employee'], x['spouses_enrolled'], x['children_enrolled'])
            employeemap[str(x['employer'])+x['employee']] = newemployee
    #if not enrolled (excludes employee)
    else:
        continue

#declares and sorts the list of employees in the map
list = []
for k, v in employeemap.items():
    list.append(v)
#sort by employee first ascending, then by total_enrolled descending since the python sort is a stable sort
list = sorted(list, key=lambda x: (x.employee))
list = sorted(list, key=lambda x: (x.total_enrolled), reverse = True)
#iterate through every employer
currcsv = 1
while currcsv <= numemployers:
    #prepares to write the csv for each employer
    csvwriter = csv.writer(open(str(currcsv) + ".csv", "w+", newline=''))
    csvwriter.writerow(["Employer", "Employee", "Total Enrolled", "Spouses Enrolled", "Children enrolled"])
    #iterate through and export data to the csv file
    for x in list:
        #if the current employee has the same employer as the current file
        if x.employer == currcsv:
            #prints employee enrollment information
            #Total enrolled is the spouses_enrolled + the children_enrolled + 1 (the employee with the plan)
            csvwriter.writerow([x.employer, x.employee, x.total_enrolled, x.spouses_enrolled, x.children_enrolled])
    #goes to the next employer
    currcsv += 1




