from normalization import * 
data = {}
template = {}

with open("compare.csv", 'r') as csvfile: #parse manual data (template should be correct)
    rows = []
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)
    
    rows[0][0] = "Columns"
    
    for row in rows:
        template[row[0]] = row[1:]

    

with open("normal_data.csv", 'r') as csvfile: #parse normalized data
    rows = []
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)
    
    rows[0][0] = "Columns"
    for row in rows:
        data[row[0]] = row[1:]

number_of_samples = len(template['Columns'])

bad_val = 0
for row in template:
    if row == "Columns": #need to skip over this row since it doesn't have any values
        continue
    for index in range(number_of_samples):
        sample = template['Columns'][index]
        val = template[row][index]

        if not val:
            val = 0

        if sample in data['Columns']:
            index_data = data['Columns'].index(sample)
            if abs(float(data[row][index_data]) - float(val)) > 0.20 and val != 0 and abs(float(data[row][index_data])-0.0) > 0.01:
                bad_val += 1
                print("bad val data:", data[row][index_data], "template", val)
        else:
            print("SAMPLE", sample)
print(bad_val)
