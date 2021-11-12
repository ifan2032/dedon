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


print(rna_values, ms_values)

ms_filters = {'298.0 -> 166.0': ['m1G', 'm2G'], '269.0 -> 137.0': ['I'], '261.0 -> 129.0': ['ho5U']}
ms_filters_keys = ['298.0 -> 166.0', '269.0 -> 137.0', '261.0 -> 129.0']
# ms_filters = {'298.0 -> 166.0': 0, '269.0 -> 137.0': 1, '261.0 -> 129.0': 2}

# is there a way to implement filers without specifying the need for timelines
