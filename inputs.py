import csv 

variables = {}
files = []
rna_values = {}
ms_values = {}
rows = []

data = { 'Columns': [] }


with open("input.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)

# row1 : variable names
var_names = []
for item in rows[0]:
    var_names.append(item.strip())

# row2: retention times
for index in range(len(rows[1])):
    rt = rows[1][index]
    name = var_names[index]
    variables[f"rt_{name}"] = float(rt)

# row3: deltas
for index in range(len(rows[2])):
    delta = rows[2][index]
    name = var_names[index]
    variables[f"delta_{name}"] = float(delta)

# last row: file names
for file_name in rows[-1]:
    files.append(file_name.strip())

for var in var_names:
    data[var] = []

for i in range(0, 4):
    name = var_names[i]
    delta = variables[f"delta_{name}"]
    rt = variables[f"rt_{name}"]
    rna_values[(rt - delta, rt + delta)] = name

for i in range(4, len(var_names)):
    name = var_names[i]
    delta = variables[f"delta_{name}"]
    rt = variables[f"rt_{name}"]
    ms_values[(rt - delta, rt + delta)] = name

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
    '352.1 -> 220.0', 
    '282.0 -> 150.0',
    '326.0 -> 194.0',
    '312.0 -> 180.0',
    '296.0 -> 164.0',
    '258.0 -> 126.0',
    '259.0 -> 127.0', 
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
    '459.0 -> 182.0', 
    '459.0 -> 327.0', 
    '318.0 -> 169.0',
    '318.0 -> 186.0',
    '302.0 -> 170.0',
    '302.0 -> 153.0',
    '316.0 -> 170.0',
    '290.0 -> 158.0',
    '410.0 -> 163.0',
    '410.0 -> 295.0',
    '413.0 -> 281.0',
    '259.0 -> 113.0', 
    '245.0 -> 191.0'
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
    ['cmnm5s2U_216'],
    ['cmnm5U'],
    ['cmnm5Um'],
    ['cmo5U'],
    ['ct6A'],
    ['D_115'],
    ['D_97'],
    ['g6A'],
    ['Gm'], 
    ['i6A'], 
    ['io6A'], 
    ['m1A', 'm2A', 'm6A', 'm8A'], 
    ['m227G'], 
    ['m22G'], 
    ['m28A', 'm62A'], 
    ['m3C', 'm5C'],
    ['m3U', 'm5U'], 
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
    ['ms2t6A_182'], 
    ['ms2t6A_327'],
    ['ncm5s2U_169'],
    ['ncm5s2U_186'],
    ['ncm5U_170'], 
    ['ncm5U_153'],
    ['ncm5Um'],
    ['nm5s2U_158'],
    ['Q_163'],
    ['Q_295'],
    ['t6A'],
    ['Um'],
    ['Y_191']
]

''' For checking row inputs are valid
for row in rows:
    print(len(row))
'''

# directly checks if input values are valid, else throws error
if len(rows[0]) != len(rows[1]) or len(rows[1]) != len(rows[2]) or len(rows[-1]) != 2:
    raise ValueError("Invalid inputs")

ms_filters = {}
for ms_filters_key in ms_filters_keys:
    ms_filters[ms_filters_key] = ms_filters_name[ms_filters_keys.index(ms_filters_key)]


