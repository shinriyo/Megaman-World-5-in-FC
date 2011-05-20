index1 = 1
index2 = 1

for x in range(100):

    if index1 != 3 and index2 != 5:
        print x + 1
    elif index1 == 3 and index2 == 5: 
       print "FizzBuzz"
       index1 = 0
       index2 = 0
    elif index1 == 3: 
       print "Fizz"
       index1 = 0
    elif index2 == 5: 
       print "Buzz"
       index2 = 0

    index1 += 1
    index2 += 1

