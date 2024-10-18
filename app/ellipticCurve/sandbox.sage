from sage.all import *

E = EllipticCurve(GF(827), [3, 30])
print("Number of points:",E.cardinality())

text = "Hello, World!"
print("plaintext",text)

P = E(2, 182)
print("P",P)

for i in range(798):
    print(f"{i} * P =", i * P)
# Generate a key pair
