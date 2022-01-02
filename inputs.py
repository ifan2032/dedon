import csv 

variables = {}

rows = []
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
files = []
for file_name in rows[-1]:
    files.append(file_name.strip())

data = { 'Columns': [] }
for var in var_names:
    data[var] = []

rna_values = {}
ms_values = {}

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

#s_filters = {'298.0 -> 166.0': ['m1G', 'm2G'], '269.0 -> 137.0': ['I'], '261.0 -> 129.0': ['ho5U'], '260.0 -> 128.0': ['s2C'], '257.0 -> 141.0': ['15N-dA'], '286.0 -> 154.0': ['ac4C'] }
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
    '352.1 -> 220.0'
]

ms_filters_name = [ 
    ['m1G', 'm2G'], 
    ['I'], 
    ['ho5U'], 
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
    ['io6A']
]

for row in rows:
    print(len(row))


ms_filters = {}
for ms_filters_key in ms_filters_keys:
    ms_filters[ms_filters_key] = ms_filters_name[ms_filters_keys.index(ms_filters_key)]

print(ms_filters)

