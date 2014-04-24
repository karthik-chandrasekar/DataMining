import sys

fp1_list = []
fp2_list = []

with open(sys.argv[1]) as fp1:
    for line in fp1.readlines():
        line = line.strip()
        fp1_list.append(line)

with open(sys.argv[2]) as fp2:
    for line in fp2.readlines():
        line = line.strip()
        fp2_list.append(line)


count = 0
for i in xrange(len(fp1_list)):
    if fp1_list[i] != fp2_list[i]:
        count +=1

print count
