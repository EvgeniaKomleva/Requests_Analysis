import json
import jsondiff
import natsort

from os import listdir
from os.path import isfile, join
#
# with open('output/0.json') as f:
#     json1 = json.load(f)
#     #print(json1)
# with open('tests/0.json') as f:
#     json2 = json.load(f)
#     #print(json2)
#
# res = jsondiff.diff(json1, json2)
# print(len(json1["DateIntervals"])-1)
# print(len(res))
#
# if res:
#     print("Diff found")
# else:
#     print("Same")


def accuracy(pred_json, true_json):
    with open(pred_json) as f:
        json1 = json.load(f)

    with open(true_json) as f:
        json2 = json.load(f)
    all = 0
    try:
        res_di = jsondiff.diff(json1["DateInterval"][0], json2["DateInterval"][0])
        all = all + len(json2["DateInterval"][0]) - 1
    except:
        res_di = {}
    try:
        res_a = jsondiff.diff(json1["Author"][0], json2["Author"][0])
        all = all+len(json2["Author"][0])
    except:
        res_a = {}
    #all = len(json2["DateInterval"][0]) - 1
    false = len(res_di)
    false_a = len(res_a)
    #print(false, false_a, all)
    if all != 0 :
        acc = (all - false)/all
    else:
        acc = 0
    return acc


files = [f for f in listdir('output')]
sorted_files = natsort.natsorted(files)
all_acc = []

for file in sorted_files:

    try:

        acc = accuracy('output/'+file, 'tests/'+file)
        if acc< 0:
            acc = acc*(-1)
        if acc != 1:
            print("In file ",file, "accuracy ",  acc)
        else:
            pass
            #print("OK", file)
        all_acc.append(acc)
    except:
        print("FileName: ", file, "ERROR")

sum = 0
for i in all_acc:

    sum = sum + i
print(sum/len(files))