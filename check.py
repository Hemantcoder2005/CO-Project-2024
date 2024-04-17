testcasenumber=input("Enter the test case number = ")

testcases = open(f"TestCases\\output\\{testcasenumber}.txt").readlines()
generated = open('out.txt').readlines()

numCases = 0
print(len(testcases),len(generated))
while(numCases < len(generated)):
    binsTest = testcases[numCases].split()
    binsGen = generated[numCases].split()
    print("\033[93mRunning instruction = ", numCases+1, "\033[00m")  

    for i in range(len(binsTest)):
        if(binsTest[i] != binsGen[i] ):
            print(f'TestCase is \033[92m{binsTest[i]}\033[00m got \033[91m{binsGen[i]}\033[00m ----> line num = \033[93m{numCases+1}\033[00m ----> reg = \033[94m{i+1}\033[00m')
            quit()
    numCases += 1

print("\033[92mAll Testcases Passed!\033[00m") 
