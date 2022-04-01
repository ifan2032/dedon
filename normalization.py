from sorted import *

sum_UV = []

print(data)
for val in range(len(data)):
    colSUM = 0

    for index in ['A', 'U', 'G', 'C']:
        colSUM += data[index][val]
    
    sum_UV.append(colSUM)

mean = {}
mean["UV"] = sum(sum_UV)/len(sum_UV)

ratio = []
for index in range(len(sum_UV)):
    ratio.append(sum_UV[index] / mean["UV"])

for row in list(data.keys())[1:]:
    mean[row] = float(sum(data[row])) / float(len(data[row]))

print(mean)
