from numpy import true_divide
from sorted import *

row_len = 0
sig_modification_size =  1

sum_UV = []

sumVals = []

for val in range(len(data['A'])):
    colSUM = 0

    tmpSumVals = []
    for index in ['A', 'U', 'G']:
        colSUM += data[index][val]
        tmpSumVals.append(data[index][val])
    sumVals.append(tmpSumVals)
    sum_UV.append(colSUM)

    if colSUM != 0:
        row_len += 1

mean = {}
mean["UV"] = sum(sum_UV)/row_len if row_len != 0 else 0

normal_data = {}
normal_data["Columns"] = data["Columns"]
ratio_UV = []

for index in range(len(sum_UV)):
    ratio_UV.append(sum_UV[index] / mean["UV"])

for row in list(data.keys())[1:]:
    normal_row = []
    for index in range(len(data[row])):
        if ratio_UV[index]:
            normal_row.append(data[row][index] / ratio_UV[index])
        else:
            normal_row.append(0)

    normal_data[row] = normal_row

for row in list(data.keys())[1:]:
    row_len = 0
    for index in range(len(data[row])):
        if data[row][index] != 0:
            row_len += 1


    mean[row] = float(sum(data[row])) / float(row_len) if row_len != 0 else 0

flagged_columns = []
samples_to_analyze = set()

for row in list(data.keys())[1:]:
    for index in range(len(data[row])):
        if mean[row] != 0:

            normal_data[row][index] /= mean[row]


            if normal_data[row][index] >= 2 or (normal_data[row][index] <= 0.5 and normal_data[row][index] != 0):
                samples_to_analyze.add(index)

upregulated_samples = [] #list upregulated samples names
downregulated_samples = [] #list downregulated samples names
upregulated_values = {} #list upregulated sample names with the significant modifications
downregulated_values = {} #list downregulated sample names with the significant modifications

# Purpose: If a modification does exist and has value 0, we want it to be flagged as downregulated
'''
modification_exists = {}
for row in list(data.keys())[1:]:
    modification_exists[row] = False
    for col in range(len(normal_data["Columns"])):
        if normal_data[row][col] > 0:
            modification_exists[row] = True
            print(row, normal_data[row])
            break
'''

print(list(normal_data.keys()))
for col in range(len(normal_data["Columns"])):
    upregulated = 0 # defined as >= 2
    downregulated = 0 # defined as nonzero and < 0.5

    upregulated_modifications = []
    downregulated_modifications = []

    for row in list(data.keys())[1:]:        
        if normal_data[row][col] >= 2:
            upregulated += 1
            upregulated_modifications.append(row)
        
        if (normal_data[row][col] <= 0.5): #and modification_exists[row]): USE LATER IF YOU WANT TO TRACK VALID MODIFICATIONS
            downregulated += 1
            downregulated_modifications.append(row)
    
    if upregulated >= sig_modification_size: #make this a parameter
        upregulated_samples.append(data["Columns"][col])
        upregulated_values[data["Columns"][col]] = upregulated_modifications
    elif downregulated >= sig_modification_size:
        downregulated_samples.append(data["Columns"][col])
        downregulated_values[data["Columns"][col]] = downregulated_modifications

upregulated_data = {}
downregulated_data = {}
for row in normal_data:
    upregulated_data[row] = []
    downregulated_data[row] = []

for sample in upregulated_samples:
    index = normal_data["Columns"].index(sample)
    for key in list(normal_data.keys()):
        upregulated_data[key].append(normal_data[key][index])

for sample in downregulated_samples:
    index = normal_data["Columns"].index(sample)
    for key in list(normal_data.keys()):
        downregulated_data[key].append(normal_data[key][index])

with open('Results/normal_data.csv', 'w') as f:
    f.write("%s, %s\n"%(key, ','.join([key for key in normal_data])))
    for col in range(len(normal_data['Columns'])):
        f.write("%s,%s\n"%('hi',','.join([str(normal_data[key][col]) for key in normal_data])))


with open('Results/downregulated.csv', 'w') as f:
    f.write("Downregulated Samples, defined as normalization < 0.5\n\n")
    for key in downregulated_values.keys():
        f.write("%s,%s\n"%(key,','.join([str(obj) for obj in downregulated_values[key]])))

with open('Results/upregulated.csv', 'w') as f:
    f.write("Upregulated Samples, defined as normalization > 2\n\n")
    for key in upregulated_values.keys():
        f.write("%s,%s\n"%(key,','.join([str(obj) for obj in upregulated_values[key]])))

with open('Results/upregulated_data.csv', 'w') as f:
    f.write("Upregulated Samples containing all modifications, defined as normalization > 2\n\n")

    for key in upregulated_data.keys():
        f.write("%s,%s\n"%(key,','.join([str(obj) for obj in upregulated_data[key]])))

with open('Results/downregulated_data.csv', 'w') as f:
    f.write("Downregulated Samples containing all modifications, defined as normalization < 0.5\n\n")

    for key in downregulated_data.keys():
        f.write("%s,%s\n"%(key,','.join([str(obj) for obj in downregulated_data[key]])))






# print out all modifications for upregulated and downregulated samples
# TODO:
# CHECK PLATE 3-3
# If UV is less than 50 percent of mean, throw out the sample