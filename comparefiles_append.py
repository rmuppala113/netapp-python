#!/usr/bin/env python

f1 = open('pswd_rh7','r')
f2 = open('pswd_rh5','r')

f1_list = []
f2_list = []
common = []

for f1line in f1.readlines():
    line_list = f1line.strip()
    f1_list.append(line_list)

for f2line in f2.readlines():
    line2_list = f2line.strip()
    f2_list.append(line2_list)

print("\nFile1 has {} lines\nFile2 has {} lines\n".format(len(f1_list),len(f2_list)))

for element in f2_list:
    if not element.startswith("root:") and element not in f1_list:
        common.append(element)

f1_list.extend(common)
f1append = open('pswd_rh7','a')
if len(common) > 0:
    print("There are {} lines that present in file2 but not in file1\n\nBelow lines from file2 will be appended to File1\n".format(len(common)))
    for l in common:
         la = l.strip()
         if la:
             print(la)
             f1append.write(la + '\n')
else:
    print("Nothing found, Both files has same data")

f1.close()
f2.close()
