import numpy as np

# Average kilometers
def avgKm(age, kms):
    mask = age!=0
    return np.where(mask, kms/age, 0)

# Kilometers bin
def kmBin(kms):
    if (kms <= 20000):
        return 1
    elif (kms <= 140000):
        return 2
    else:
        return 3

# Average kilometers bin
def avgKmBin(avgKms):
    if avgKms <= 10000:
        return 1
    elif avgKms <= 20000:
        return 2
    else:
        return 3