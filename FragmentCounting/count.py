import matplotlib.pyplot as plt
import math
import statistics
import re

infile = open("output.fa")
sequence = infile.read()
dna = sequence[128:]

sequence_arrays = sequence.split("\n")
all_cuts = [[0] for i in range(len(sequence_arrays))]

print("0")
# finda and append different cut positions for AbcI
for i in range(1, len(sequence_arrays), 2):

    
    for match in re.finditer(r"CT", sequence_arrays[i]):#begins with A followed by any one character [ATGC]and then TAAT
        if i == 1:
            print(sequence_arrays[i][match.start(): match.start() + 3], match.start())
        all_cuts[i//2].append(match.start() + 3) #ANT*AAT, finding position is A therefore +3 for ANT


print(all_cuts[0])
print("a")
# add the finalend position i.e. length of dna
for all_cut in all_cuts:
    all_cut.append(len(all_cut))

sorted_cuts = [sorted(all_cut) for all_cut in all_cuts] # Sort the cut position in ascending order so that we get length of each fragements correct

fragment_sizes = []
for sorted_cut in sorted_cuts:
    for i in range(1,len(sorted_cut)):
        this_cut_position = sorted_cut[i]
        previous_cut_position = sorted_cut[i-1]
        fragment_size = this_cut_position - previous_cut_position
        fragment_sizes.append(fragment_size)

print("c")


plt.hist(fragment_sizes, bins=50, range=[0,100])
plt.axvline(statistics.mean(fragment_sizes), color='k', linestyle='dashed', linewidth=1)
plt.show()