na = 254032
nb = 789860


import numpy as np


# 1
ia = int(list(str(na))[0])
ib = int(list(str(nb))[0])

c = 0
for i0 in range(ia, ib+1):
    for i1 in range(i0, 10):
        for i2 in range(i1, 10):
            for i3 in range(i2, 10):
                for i4 in range(i3, 10):
                    for i5 in range(i4, 10):
                        a = np.array([i0, i1, i2, i3, i4, i5])
                        n = int(''.join(a.astype(str)))
                        if na <= n <= nb:
                            if (a[:-1] == a[1:]).any():
                                c += 1
print(c)

# 2
c = 0
for i0 in range(ia, ib+1):
    for i1 in range(i0, 10):
        for i2 in range(i1, 10):
            for i3 in range(i2, 10):
                for i4 in range(i3, 10):
                    for i5 in range(i4, 10):
                        a = np.array([i0, i1, i2, i3, i4, i5])
                        n = int(''.join(a.astype(str)))
                        if na <= n <= nb:
                            if ((i0 == i1 and i1 != i2) or
                                (i1 == i2 and i0 != i1 and i2 != i3) or
                                (i2 == i3 and i1 != i2 and i3 != i4) or
                                (i3 == i4 and i2 != i3 and i4 != i5) or
                                (i4 == i5 and i3 != i4)
                               ):
                                c += 1
print(c)
