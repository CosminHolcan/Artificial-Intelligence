import math
import random


n = 5000
pairs = []
for _ in range(n):
    x = random.random() * 20 - 10
    y = random.random() * 20 - 10
    value = math.sin(x + y / math.pi)
    pairs.append(((x, y), value))
with open("mydataset.txt", "w") as file:
    file.write(f"{n}\n")
    for pair in pairs:
        file.write(f"{pair[0][0]},{pair[0][1]},{pair[1]}\n")