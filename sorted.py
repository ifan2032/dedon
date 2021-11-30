import csv
import copy 

from inputs import *


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
        #tmp_data = { (C-deltaC, C+deltaC): '-', (G-deltaG, G+deltaG): '-', (A-deltaA, A+deltaA): '-', (U-deltaU, U+deltaU): '-'}
        tmp_data = copy.deepcopy(rna_values)
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
        ms_tmp = {} 
        for i in range(4, len(var_names)):
            name = var_names[i]
            ms_tmp[name] = []
        ms_data[column] = ms_tmp
        
    filename = files[1]
    fields = []
    rows = []
    
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)

        for row in csvreader:
            rows.append(row)
    divider_indices = [ [] for _ in range(len(ms_filters.keys())) ]
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
                            divider_indices[ms_filters_keys.index(j)].append(i)

    for k in range(len(divider_indices)):
        countera = 0
        a = 0
        for divider_index in divider_indices[k]:
            countera += 1
            stop_index = divider_indices_two[divider_indices_two.index(divider_index)+1]
            curRow = 0 
            counter = 0
            a += 1
            for index in range(divider_index+2, stop_index):
                row = rows[index]


                if len(row) == 0:
                    continue
                rt = float(row[3])

                name = row[0].split('\\')[-1].strip()
                
                for (start, end) in list(ms_values.keys()):
                    if start <= rt and rt <= end and ms_values[(start, end)] in ms_filters[ms_filters_keys[k]]:
                        ms_data[name][ms_values[(start, end)]].append(float(row[6]))

    
    for row in data['Columns']:
        values = ms_data[row]

        for strain in values:
            if len(values[strain]) != 0:
                data[strain].append(max(values[strain]))
            else:
                data[strain].append(values[strain])
            ''' 
            if (len(values[strain]) == 1):
                data[strain].append(values[strain][0])
            else:
                data[strain].append(max(values[strain]))
            '''
# Call Methods 

parseUV()
parseMS()

print("#############---- Results ----##############")

#find highest peak or closest to retention time

lengths = {}

for pair in data:
    s = 0

    for area_val in data[pair]:
        if area_val == '-' or area_val == []:
            s += 1
        
        if type(area_val) == list:
            s -= (len(area_val) - 1)

            '''
            if pair == 'ho5U':
                print(data["Columns"][data[pair].index(area_val)])
            '''

    lengths[pair] = len(data[pair]) - s

print(lengths)

# Export 

with open('results2.csv', 'w') as f:
    for key in data.keys():
        f.write("%s,%s\n"%(key,data[key]))



