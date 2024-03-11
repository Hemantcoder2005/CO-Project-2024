f1=open("output.txt").readlines()
f2=open("output1.txt").readlines()


for i in range(len(f1)):
    if f1[i]!=f2[i]:
        print("Error at line ",i+1)
        exit()
print("All testcase passed!")