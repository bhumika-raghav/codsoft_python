 # 9. count vowels

s = input()
count=0

for ch in s:
  if ch in "aeiouAEIOU":
    count+=1

    print(count)