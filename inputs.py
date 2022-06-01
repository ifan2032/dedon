import csv

from numpy import number 

variables = {}
files = []
rna_values = {}
ms_values = {}
rows = []
modifications = []

data = { 'Columns': [] }

'''
input.csv contains data regarding modifications, retention times, retention windows
modification.csv contains table with all modifications
'''

with open("Inputs/input.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)

with open("Inputs/modification.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        modifications.append(row)

# row1 : variable names
var_names = []
for item in rows[0]:
    var_names.append(item.strip())

# row2: retention times
for index in range(len(rows[1])):
    rt = rows[1][index]
    name = var_names[index]
    variables[f"rt_{name}"] = float(rt.strip())

# row3: deltas
for index in range(len(rows[2])):
    delta = rows[2][index]
    name = var_names[index]
    variables[f"delta_{name}"] = float(delta.strip())

# last row: file names
for file_name in rows[-1]:
    files.append(file_name.strip())

for var in var_names:
    # we want to put G and A under the same modification due to how close their retention times are
    if var == 'GA':
        data['G'] = []
        data['A'] = []
    else:
        data[var] = []

print("data", data)

for i in range(0, 3):
    name = var_names[i]
    delta = variables[f"delta_{name}"]
    rt = variables[f"rt_{name}"]
    rna_values[(rt - delta, rt + delta)] = name

for i in range(3, len(var_names)):
    name = var_names[i]
        
    delta = variables[f"delta_{name}"]
    rt = variables[f"rt_{name}"]

    if (rt - delta, rt + delta) in ms_values:
        ms_values[(rt - delta, rt + delta)].append(name)
    else:
        ms_values[(rt - delta, rt + delta)] = [name]


dummy_keys = []
dummy_name = []

for row in modifications:
    name = row[0]
    start = row[1].strip()
    end = row[2].strip()
    
    if '.' not in start:
        start += '.0'
    if '.' not in end:
        end += '.0'
    
    transition = f"{start} -> {end}"
    
    if transition in dummy_keys:
        dummy_name[dummy_keys.index(transition)].append(name)
    else:
        dummy_keys.append(transition)
        dummy_name.append([name])

ms_filters_keys = [
    '298.0 -> 166.0', 
    '269.0 -> 137.0', 
    '261.0 -> 129.0', 
    '260.0 -> 128.0',
    '257.0 -> 141.0', 
    '286.0 -> 154.0', 
    '346.0 -> 214.0', 
    '282.0 -> 136.0', 
    '258.0 -> 112.0', 
    '303.1 -> 171.0', 
    '317.0 -> 171.0', 
    '348.0 -> 141.0',
    '348.0 -> 216.0',
    '332.0 -> 200.0',
    '346.1 -> 200.1',
    '319.0 -> 187.0',
    '395.1 -> 236.1',
    '247.0 -> 115.0',
    '247.0 -> 97.0', 
    '369.1 -> 136.1', 
    '298.0 -> 152.0', 
    '336.0 -> 204.0',
    '322.1 -> 190.1', 
    '342.3 -> 210.0',
    '352.1 -> 220.0', 
    '372.1 -> 240.1',
    '282.0 -> 150.0',
    '326.0 -> 194.0',
    '312.0 -> 180.0',
    '296.0 -> 164.0',
    '258.0 -> 126.0',
    '259.0 -> 127.0',
    '272.1 -> 126.1',
    '275.0 -> 143.0',
    '273.0 -> 127.0', 
    '296.1 -> 150.0', 
    '427.0 -> 295.0', 
    '317.2 -> 185.1', 
    '331.1 -> 153.1',
    '331.1 -> 185.1', 
    '333.0 -> 201.0',
    '333.0 -> 315.0',
    '304.0 -> 172.0',
    '304.0 -> 273.0',
    '382.2 -> 250.1',
    '459.0 -> 182.0', 
    '459.0 -> 327.0', 
    '318.0 -> 169.0',
    '318.0 -> 186.0',
    '302.0 -> 170.0',
    '302.0 -> 153.0',
    '316.0 -> 170.0',
    '290.0 -> 158.0',
    '426.0 -> 163.0',
    '426.0 -> 295.0',
    '312.0 -> 163.0',
    '312.0 -> 295.0',
    '410.0 -> 163.0',
    '410.0 -> 295.0',
    '255.1 -> 123.1',
    '275.1 -> 129.0',
    '307.0 -> 175.0',
    '413.0 -> 281.0',
    '259.0 -> 113.0', 
    '245.0 -> 191.0',
    '348.0 -> 255.0',
    '395.1 -> 119.0', 
    '395.1 -> 162.0',
    '539.2 -> 407.0',
    '283.0 -> 137.0'
]

ms_filters_name = [ 
    ['m1G', 'm2G', 'm7G'], 
    ['I'], 
    ['ho5U', 's2U', 's4U'], 
    ['s2C'], 
    ['15N-dA'], 
    ['ac4C'], 
    ['acp3U'], 
    ['Am'], 
    ['Cm'], 
    ['cm5U'], 
    ['cm5Um'], 
    ['cmnm5s2U_141'],
    ['cmnm5s2U_216', 'acp3D_216'],
    ['cmnm5U'],
    ['cmnm5Um'],
    ['cmo5U'],
    ['ct6A'],
    ['D_115'],
    ['D_97'],
    ['g6A'],
    ['Gm'], 
    ['i6A'],
    ['imG-14'],
    ['inm5U'],
    ['io6A'], 
    ['k2C'],
    ['m1A', 'm2A', 'm6A', 'm8A'], 
    ['m227G'], 
    ['m22G'], 
    ['m28A', 'm62A'], 
    ['m3C', 'm5C'],
    ['m3U', 'm5U'],
    ['m4Cm/m5Cm'], 
    ['m5s2U', 'mo5U'], 
    ['m5Um'], 
    ['m6Am'], 
    ['m6t6A'], 
    ['mcm5U'],
    ['mcm5Um_153'], 
    ['mcm5Um_185'], 
    ['mcmo5U_201'],
    ['mcmo5U_315'], 
    ['mnm5s2U_172'], 
    ['mnm5s2U_273'],
    ['ms2i6A'],
    ['ms2t6A_182'], 
    ['ms2t6A_327'],
    ['ncm5s2U_169'],
    ['ncm5s2U_186'],
    ['ncm5U_170'], 
    ['ncm5U_153'],
    ['ncm5Um'],
    ['nm5s2U_158'],
    ['oQ_163'],
    ['oQ_295'],
    ['preQ1_163'],
    ['preQ1_295'],
    ['Q_163'],
    ['Q_295'],
    ['rNA'],
    ['s2Um'],
    ['se2U'],
    ['t6A'],
    ['Um'],
    ['Y_191'],
    ['cmnm5s2U_255'],
    ['ct6A_119'],
    ['ct6A_162'],
    ['gluQ'],
    ['Im']
]

ms_filters_keys = dummy_keys
ms_filters_name = dummy_name


''' 
Try to have a separate list containing all modifications you would like to run

'''
# directly checks if input values are valid, else throws error
if len(rows[0]) != len(rows[1]) or len(rows[1]) != len(rows[2]):
    raise ValueError("Invalid inputs")

ms_filters = {}
for ms_filters_key in ms_filters_keys:
    ms_filters[ms_filters_key] = ms_filters_name[ms_filters_keys.index(ms_filters_key)]

rows = []


with open(files[2], 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row[2:]) # FIX THIS LINE
    
    init_modifications = []
    init_modifications_index = []
    for x in range(len(rows[0])):
        if rows[0][x] and rows[0][x] != 'Sample':
            init_modifications.append(rows[0][x].split(" ")[0])
            init_modifications_index.append(int(x))

    columns = [row[0] for row in rows] #changed this when batch table was modified
    data["Columns"] = columns[2:]

    modifications = []
    modifications_index = []

    for mod in list(data.keys())[1:]:
        if mod in ['C', 'U', 'G', 'A']: #we don't want to process UV
            continue
        else:
            index = init_modifications.index(mod)
            modifications.append(init_modifications[index])
            modifications_index.append(init_modifications_index[index])

    for modification in modifications:
        data[modification] = []
    
    for row in rows[2:]:
        for index in range(len(modifications_index)):
            real_index = modifications_index[index]
            
            val = row[real_index+1]
            modification = modifications[index]

            if val:
                val = float(val)

                if float(row[real_index+1]) <= 100 or float(row[real_index+2]) < 5: #make sure t
                    val = 0
            else:
                val = 0
            
            data[modification].append(val)

# fill up empty modifications
number_of_samples = len(data['Columns'])
for row in data:
    if len(data[row]) == 0 and not row in ['Columns']:
        data[row] = [0] * number_of_samples

# peak area less than 100 S/N less than 3 --> make into 0 MAKE



