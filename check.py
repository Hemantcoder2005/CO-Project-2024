testcases=open("output.txt").readlines()
generated=open('out.txt').readlines()

numCases=0

while(numCases<len(generated)):
    binsTest=testcases[numCases].split()
    binsGen=generated[numCases].split()
    for i in range(len(binsTest)):
        if(binsTest[i]!=binsGen[i]):
            print(f'TestCase is {binsTest[i]} Your is {binsGen[i]}----> line num ={numCases+1}----> reg = {i+1}')
            quit()
    numCases+=1
print("All test case passed")

