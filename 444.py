count = 0
for number in range(400):
    for num in str(number):
        if int(num) == 4:
            count += 1
print(count)