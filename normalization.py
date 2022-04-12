from sorted import *

sum_UV = []
row_len = 0

for val in range(len(data['A'])):
    colSUM = 0

    for index in ['A', 'U', 'G']:
        colSUM += data[index][val]

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
        normal_row.append(data[row][index] / ratio_UV[index])
    normal_data[row] = normal_row

for row in list(data.keys())[1:]:
    row_len = 0
    for index in range(len(data[row])):
        if data[row][index] != 0:
            row_len += 1

    mean[row] = float(sum(data[row])) / float(row_len) if row_len != 0 else 0

flagged_columns = []
samples_to_analyze = set()
bad_samples = []

for row in list(data.keys())[1:]:
    for index in range(len(data[row])):
        if mean[row] != 0:
            normal_data[row][index] /= mean[row]

            if normal_data[row][index] >= 2 or (normal_data[row][index] <= 0.5 and normal_data[row][index] != 0):
                samples_to_analyze.add(index)

for col in range(len(normal_data["Columns"])):
    number_of_sig_values = 0
    for row in list(data.keys())[1:]:
        if normal_data[row][col] >= 2 or (normal_data[row][col] <= 0.5 and normal_data[row][col] != 0):
            number_of_sig_values += 1
    
    if number_of_sig_values >= 5: #make this a parameter
        bad_samples.append(data["Columns"][col])



with open('normal_data.csv', 'w') as f:
    for key in normal_data.keys():
        f.write("%s,%s\n"%(key,','.join([str(normal_data[key][index]) for index in samples_to_analyze])))
    f.write("\n")
    f.write("%s,%s\n"%("Bad Samples",','.join([str(index) for index in bad_samples])))


# TODO:

# greater than 2 or less 0.5
# add a modification list for future analysis