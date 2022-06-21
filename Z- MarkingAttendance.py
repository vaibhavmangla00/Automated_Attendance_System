'''
FOURT PART OF THE PROJECT
'''


namelist = {}

with open("Attendance of Students", "r") as ar:
    lines = ar.readlines()
    for line in lines[10:]:
        name = line.split(',')[0]
        time = line.split(',')[1]
        date = line.split(',')[2]
        if name in lines[lines.index(line)-7] and name in lines[lines.index(line)-6] and name in lines[lines.index(line)-5] and name in lines[lines.index(line)-4] and name in lines[lines.index(line)-3] and name in lines[lines.index(line)-2] and name in lines[lines.index(line)-1]:
            if name not in namelist.keys():
                namelist[name] = time
                # Attendance_of_Students.csv must already exist with Name and Time as columns
                with open('Attendance_of_Students.csv', 'a') as f:
                    f.writelines(f"{name},{time},{date}")

print(namelist)
