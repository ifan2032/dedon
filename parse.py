f = open('test.txt', 'r')
content = f.read()

# splice txt file to find data of interest 
index_to_cut = content.find('[PEAK]')
content = content[index_to_cut:]

peaks_arr = content.split('[PEAK]')
peaks_arr_dict = []
peaks_arr_info = []

# parses txt file into dictionary for easy handling
for i in range(len(peaks_arr)):
    if len(peaks_arr[i]) != 0:
        fields_arr = peaks_arr[i].split("\n")
        fields_arr = fields_arr[2:12]
        dict_info = {}
        for j in range(len(fields_arr)):
            field_process_arr = fields_arr[j].split("\t")
    
            key = field_process_arr[0]
            if len(field_process_arr) == 3:
                item = [float(field_process_arr[1]), float(field_process_arr[2])]
            else:
                item = float(field_process_arr[1])
                
                dict_info[key] = item
        peaks_arr_info.append(dict_info)

    else:
        peaks_arr_info.append({})

# assigns area values to C, G, U, A
rna_values = { (2.0, 2.4): 'C', (3.7, 4.2): 'G', (4.4, 4.7): 'A', (5.8, 6.2): 'T'}
data = { 'C': [], 'G': [], 'A': [], 'T': []}

# starts to classify peaks to C, G, U, A
for i in range(len(peaks_arr_info)):
    val = peaks_arr_info[i]
    if len(val) > 0:
        area = val['AreaAbs']
        time = val['Time']
        
        for (start, end) in rna_values:
            if start <= time and time <= end:
                data[rna_values[(start, end)]].append(area)
                break

print(data)
