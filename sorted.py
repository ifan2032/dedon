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
        area_data = copy.deepcopy(rna_values)
        for key in area_data:
            area_data[key] = []
        
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
                        area_data[(start, end)].append(area)
        
        for (start, end) in area_data:
            val = area_data[(start, end)]
            name = rna_values[(start, end)]
            
            if name == 'GA':
                if len(val) <= 1:
                    data['G'].append(0)
                    data['A'].append(0)
                else:
                    data['G'].append(val[0])
                    data['A'].append(val[1])
            elif len(val) == 0:
                data[rna_values[(start, end)]].append(0)
            else:
                data[rna_values[(start, end)]].append(max(val))
    return

def parseMS():

    ms_data = {}
    for column in data['Columns']:
        ms_tmp = {} 
        for i in range(3, len(var_names)):
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
    divider_indices_two.append(len(rows))
    for k in range(len(divider_indices)):
        countera = 0
        a = 0
        for divider_index in divider_indices[k]:
            countera += 1
            stop_index = divider_indices_two[(divider_indices_two.index(divider_index)+1)]
            curRow = 0 
            counter = 0 # 
            a += 1
            for index in range(divider_index+2, stop_index):
                row = rows[index]

                if len(row) == 0:
                    continue
                rt = float(row[3])

                name = row[0].split('\\')[-1].strip()
                
                for (start, end) in list(ms_values.keys()):
                    for value in ms_values[(start, end)]:
                        if start <= rt and rt <= end and value in ms_filters[ms_filters_keys[k]]:
                            ms_data[name][value].append(float(row[6]))

    
    for row in data['Columns']:
        values = ms_data[row]

        for strain in values:
            if len(values[strain]) != 0:
                data[strain].append(max(values[strain]))
            else:
                #print("values strain", values[strain])
                data[strain].append(0)

# Call Methods 

parseUV()
parseMS()

print("#############---- Results ----##############")

#find highest peak 

lengths = {}

for pair in data:
    s = 0

    for area_val in data[pair]:
        if area_val == '-' or area_val == []:
            s += 1
        
        if type(area_val) == list:

            s -= (len(area_val) - 1)

    lengths[pair] = len(data[pair]) - s

print("#############---- End ----##############")


# Export 


with open('results.csv', 'w') as f:
    for key in data.keys():
        f.write("%s,%s\n"%(key,','.join([str(obj) for obj in data[key]])))

