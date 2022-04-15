MIN_DELAY = 0.00099
MAX_DELAY = 0.00001
STEPS_PER_MM_DEFAULT = 19.0375

cm = 10
print(0.00099 - 0.00001)

steps = int((float(cm) * 10) * int(STEPS_PER_MM_DEFAULT))

print(steps)

if steps > 600:
    print("we can accelerate")

