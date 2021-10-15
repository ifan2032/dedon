import csv

delta = 0.08
C, U, G, A, m1G, m2G, I, ho5U = (0.6, 1.2, 3.3, 3.6, 4.68, 4.91, 3.14, 0.90)
rna_values = { (C-delta, C+delta): 'C', (G-delta, G+delta): 'G', (A-delta, A+delta): 'A', (U-delta, U+delta): 'U'}
data = { 'C': [], 'G': [], 'A': [], 'U': [], 'm1G': [], 'm2G': [], 'I': [], 'ho5U': []}
ms_filters = ['298.0 -> 166.0', '269.0 -> 137.0', '261.0 -> 129.0']


def parseUV():
    filename = "data2.csv"
    
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

    time_index, area_index = rows[0].index("RT"), rows[0].index("Area")

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
    return

def parseMS():
    filename = "data1.csv"
    
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
            for col in row:
                for ms_filter in ms_filters:
                    if ms_filter in col:
                        divider_indices.append(i)
        
    print(divider_indices)

parseUV()
parseMS()



# print results
print("#############---- Results ----##############")
for pair in data:
    s = f"{pair} || "
    for area_val in data[pair]:
        s += f"{area_val}, "
    s += "\n"
    print(s)
