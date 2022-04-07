from sorted import *

sum_UV = []

for val in range(len(data['A'])):
    colSUM = 0

    for index in ['A', 'U', 'G', 'C']:
        colSUM += data[index][val]
    
    sum_UV.append(colSUM)

mean = {}
mean["UV"] = sum(sum_UV)/len(sum_UV)

normal_data = {}
ratio_UV = []
for index in range(len(sum_UV)):
    ratio_UV.append(sum_UV[index] / mean["UV"])

for row in list(data.keys())[1:]:
    normal_row = []
    for index in range(len(data[row])):
        normal_row.append(data[row][index] / ratio_UV[index])
    normal_data[row] = normal_row

for row in list(data.keys())[1:]:
    mean[row] = float(sum(data[row])) / float(len(data[row]))

for row in list(data.keys())[1:]:
    for index in range(len(data[row])):
        if mean[row] != 0:
            normal_data[row][index] /= mean[row]

with open('normal_data.csv', 'w') as f:
    for key in normal_data.keys():
        f.write("%s,%s\n"%(key,','.join([str(obj) for obj in normal_data[key]])))