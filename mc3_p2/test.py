import numpy as np
T = np.array([0.00001]*40000).reshape(100,4,100)
summ=0
for i in range(0,100):
	T[12,2,i] = np.random.randint(12,180)


temps = 12
tempa = 2
print T[12,2,:]
print np.argmax(T[temps,tempa,:])
