import csv

# Exclude everything that starts with cpd 

# Change As Necessary
deltaG, deltaA, deltaU, deltaC, deltaI, delta = 0.15, 0.10, 0.10, 0.05, 0.4, 0.15
C, U, G, A, m1G, m2G, I, ho5U = (0.6, 1.2, 3.3, 3.5, 4.67, 4.922, 3.123, 0.90)

rna_values = { (C-deltaC, C+deltaC): 'C', (G-deltaG, G+deltaG): 'G', (A-deltaA, A+deltaA): 'A', (U-deltaU, U+deltaU): 'U'}
data = { 'Columns': [], 'C': [], 'G': [], 'A': [], 'U': [], 'm1G': [], 'm2G': [], 'I': [], 'ho5U': []}
ms_filters = {'298.0 -> 166.0': 0, '269.0 -> 137.0': 1, '261.0 -> 129.0': 2}
ms_values = {(m1G-delta, m1G+delta): 'm1G', (m2G-delta, m2G+delta): 'm2G', (I-deltaI, I+deltaI): 'I', (ho5U-delta, ho5U+delta): 'ho5U'}

files = ["LCMS1//96plate//02_A1_UV_104.csv", "LCMS1//96plate//02_A1_MS_104.csv"]

def parseUV():
    filename = files[0]
    
    fields = []
    rows = []
    
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)
        
    divider_indices = []
    for i in range(len(rows)):
        row = rows[i]
        if (len(row) == 2):
            divider_indices.append(i)

    divider_indices.append(len(rows))
    divider_indices.insert(0, 0)

    time_index, area_index = rows[0].index("RT"), rows[0].index("Area")

    for index in range(len(divider_indices)-1):
        tmp_data = { (C-deltaC, C+deltaC): '-', (G-deltaG, G+deltaG): '-', (A-deltaA, A+deltaA): '-', (U-deltaU, U+deltaU): '-'}

        for row_index in range(divider_indices[index], divider_indices[index+1]):
            row = rows[row_index]

            if row_index == divider_indices[index]:
                info = row[0].split('\\')
                data['Columns'].append(info[-1].strip())

            if not "RT" in row and not "Area" in row and len(row) > max(time_index, area_index):
                time = float(row[time_index])
                area = float(row[area_index])
                for (start, end) in rna_values:
                    if start <= time and time <= end:
                        tmp_data[(start, end)] = area
                        break
        
        for (start, end) in tmp_data:
            val = tmp_data[(start, end)]
            
            data[rna_values[(start, end)]].append(val)
    return

def parseMS():

    ms_data = {}
    for column in data['Columns']:
        ms_data[column] = { 'm1G': [], 'm2G': [], 'I': [], 'ho5U': [] } # m1G, m2G, I, ho5U
    
    filename = files[1]
    fields = []
    rows = []
    
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)

        for row in csvreader:
            rows.append(row)

    divider_indices = [ [], [], [] ] #[0] stores 298->166, [1] stores 269->137, [2] stores 261->129 
    divider_indices_two = []
    for i in range(len(rows)):
        row = rows[i]

        if (len(row) == 2):
            divider_indices_two.append(i)

            tag = row[-1][0:4]
            if 'Cpd' not in tag:
                for col in row:
                    for j in list(ms_filters.keys()):
                        if j in col:
                            divider_indices[ms_filters[j]].append(i)

    for k in range(len(divider_indices)):
        countera = 0
        a = 0
        for divider_index in divider_indices[k]:
            countera += 1
            stop_index = divider_indices_two[divider_indices_two.index(divider_index)+1]

            isFound = False 
            curRow = 0 
            counter = 0
            a += 1
            for index in range(divider_index+2, stop_index):
                row = rows[index]

                if len(row) == 0:
                    continue
                rt = float(row[3])

                name = row[0].split('\\')[-1].strip()
                
                if k == 0:
                    for (start, end) in list(ms_values.keys())[0:2]:
                        if start <= rt and rt <= end:
                            print(rt, start, end)
                            data[ms_values[(start, end)]].append(float(row[6]))
                            ms_data[name][ms_values[(start, end)]].append(float(row[6]))
                            isFound = True
                elif k == 1:
                    for (start, end) in list(ms_values.keys())[2:3]:
                        if start <= rt and rt <= end and not isFound:
                            data[ms_values[(start, end)]].append(float(row[6]))
                            ms_data[name][ms_values[(start, end)]].append(float(row[6]))
                            isFound = True
                else:
                    counter += 1
                    for (start, end) in list(ms_values.keys())[3:4]:
                        if start <= rt and rt <= end and not isFound and float(row[6]) > 200:
                            data[ms_values[(start, end)]].append(float(row[6]))
                            ms_data[name][ms_values[(start, end)]].append(float(row[6]))
                            isFound = True

                if isFound:
                    break
            
    for keys,values in ms_data.items():
        print(keys)
        print(values)
parseUV()
parseMS()

print("#############---- Results ----##############")
lengths = {}

for pair in data:
    s = 0
    for area_val in data[pair]:
        if area_val == '-':
            s += 1
    lengths[pair] = len(data[pair]) - s

print(lengths)


with open('results2.csv', 'w') as f:
    for key in data.keys():
        f.write("%s,%s\n"%(key,data[key]))

