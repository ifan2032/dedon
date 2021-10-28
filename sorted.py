import csv

deltaG = 0.15
deltaA = 0.10
deltaU = 0.10
deltaC = 0.05
delta = 0.05
deltaI = 0.10
C, U, G, A, m1G, m2G, I, ho5U = (0.6, 1.2, 3.3, 3.5, 4.67, 4.905, 3.123, 0.90)
rna_values = { (C-deltaC, C+deltaC): 'C', (G-deltaG, G+deltaG): 'G', (A-deltaA, A+deltaA): 'A', (U-deltaU, U+deltaU): 'U'}
data = { 'C': [], 'G': [], 'A': [], 'U': [], 'm1G': [], 'm2G': [], 'I': [], 'ho5U': []}
ms_filters = {'298.0 -> 166.0': 0, '269.0 -> 137.0': 1, '261.0 -> 129.0': 2}
ms_values = {(m1G-delta, m1G+delta): 'm1G', (m2G-delta, m2G+delta): 'm2G', (I-deltaI, I+deltaI): 'I', (ho5U-delta, ho5U+delta): 'ho5U'}

def parseUV():
    filename = "LCMS1//101421 Leon practice/02_WT_rRNA_UV_5.csv"
    
    # initializing the titles and rows list
    fields = []
    rows = []
    
    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
        
    divider_indices = []
    for i in range(len(rows)):
        row = rows[i]

        if (len(row) == 2):
            divider_indices.append(i)

    divider_indices.append(len(rows))
    divider_indices.insert(0, 0)

    print(divider_indices)

    time_index, area_index = rows[0].index("RT"), rows[0].index("Area")

    for index in range(len(divider_indices)-1):
        tmp_data = { (C-deltaC, C+deltaC): '-', (G-deltaG, G+deltaG): '-', (A-deltaA, A+deltaA): '-', (U-deltaU, U+deltaU): '-'}

        for row_index in range(divider_indices[index], divider_indices[index+1]):
            row = rows[row_index] 
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

            

    '''
    for row in rows[1:]:
        # parsing each column of a row
        #for col in row:
        #    print("%10s"%col),
        if not "RT" in row and not "Area" in row and len(row) > max(time_index, area_index):
            time = float(row[time_index])
            area = float(row[area_index])
            for (start, end) in rna_values:
                if start <= time and time <= end:
                    data[rna_values[(start, end)]].append(area)
                    break
    ''' 

    return

def parseMS():
    filename = "LCMS1//101421 Leon practice/02_WT_rRNA_MS_5.csv"
    
    # initializing the titles and rows list
    fields = []
    rows = []
    
    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    divider_indices = [ [], [], [] ] #[0] stores 298->166, [1] stores 269->137, [2] stores 261->129 
    divider_indices_two = []
    for i in range(len(rows)):
        row = rows[i]

        if (len(row) == 2):
            divider_indices_two.append(i)

            for col in row:
                for j in list(ms_filters.keys()):
                    if j in col:
                        divider_indices[ms_filters[j]].append(i)

    for k in range(len(divider_indices)):
        countera = 0
        for divider_index in divider_indices[k]:
            countera += 1
            stop_index = divider_indices_two[divider_indices_two.index(divider_index)+1]

            isFound = False 
            curRow = 0 
            counter = 0

            for index in range(divider_index+2, stop_index):
                row = rows[index]

                if len(row) == 0:
                    continue
                rt = float(row[3])

                if k == 0:
                    for (start, end) in list(ms_values.keys())[0:2]:
                        if start <= rt and rt <= end:
                            data[ms_values[(start, end)]].append(float(row[6]))
                elif k == 1:
                    for (start, end) in list(ms_values.keys())[2:3]:
                        if start <= rt and rt <= end and not isFound:
                            data[ms_values[(start, end)]].append(float(row[6]))
                            isFound = True
                else:
                    counter += 1
                    for (start, end) in list(ms_values.keys())[3:4]:
                        if start <= rt and rt <= end and not isFound and float(row[6]) > 200:
                            data[ms_values[(start, end)]].append(float(row[6]))
                            isFound = True

                if isFound:
                    break
            
                




    

parseUV()
parseMS()



# print results
print("#############---- Results ----##############")
lengths = []

for i in range(len(data["A"])):
    s = ""
    for j in ['U', 'G', 'A']:
        s += f"{data[j][i]}, "
    s += "\n"
    print(s)

print(len(data['m1G']), len(data['I']), len(data['ho5U']))

'''
for pair in data:
    s = f"{pair} || "
    for area_val in data[pair]:
        s += f"{area_val}, "
    lengths.append(len(data[pair]))
    s += "\n"
    print(s)
print(lengths)'''


with open('results2.csv', 'w') as f:
    for key in data.keys():
        f.write("%s,%s\n"%(key,data[key]))

