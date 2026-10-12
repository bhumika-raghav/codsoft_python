'''# Count even number in list 
arr=list(map(int,input().split()))
count=0

for x in arr:
    if x % 2==0:
        count+=1

print(count)'''

'''# Prime number check

n=int(input())
count=0

for i in range(1,n+1):
    if n%i==0:
        count+=1

if count==2:
    print("prime")
else:
    print("not prime")'''

'''#fibonacci series
n=int(input())

a=0
b=1
for i in range(n):
    print (a,end=" ")
    a,b=b , a + b'''

'''#sum of digits

n=input()
total=0

for digit in n :
    total+=int(digit)

    print (total)'''

# remove duplicates from list

arr = list(map(int,input().split()))

result = []

for x in arr:
    if x not in result:
        result.append(x)

print(*result)        