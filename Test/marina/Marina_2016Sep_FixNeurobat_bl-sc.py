
data_dict = {}
outlist = []

with open('/data/data02/sulantha/Marina_Sep_2016/NEUROBAT_toBeFIX.csv', 'r') as file:
    next(file)
    for line in file:
        row = line.split(',')
        rid = row[0]
        vis = row[1]
        if rid not in data_dict:
            data_dict[rid] = {vis:row}
        else:
            data_dict[rid][vis] = row

for k in data_dict:
    if 'sc' not in data_dict[k]:
        continue
    if 'bl' not in data_dict[k]:
        continue

    sc_data = data_dict[k]['sc']
    bl_data = data_dict[k]['bl']

    for i in range(len(bl_data)):
        if bl_data[i] == '' and sc_data[i] != '':
            data_dict[k]['bl'][i] = sc_data[i]


for k in data_dict:
    for k2 in data_dict[k]:
        outlist.append(data_dict[k][k2])

thefile = open('/data/data02/sulantha/Marina_Sep_2016/NEUROBAT_FIXED.csv', 'w')
for item in outlist:
  thefile.write("%s\n" % item)