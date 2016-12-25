import numpy as np
import pylab as pl


def OVC(N, V, C):
	return np.sqrt((8 / N) * (np.log(4 / C) + V * np.log(2 * N)  ))

def VVC(N, V, C):
	return np.sqrt((16 / N) * (np.log(2 / np.sqrt(C)) +  V * np.log(1 * N)))

def RPB(N, V, C):
	return np.sqrt((2 / N) * (np.log(2 * N) + V * np.log(1 * N))) + np.sqrt((2 / N) * np.log(1 / C)) + 1 / N

def PVB(N, V, C):
	return (1 / N) + np.sqrt((1 / (N^2)) + (1 / N) * (np.log(6 / C ) +  V * np.log(2 * N)))

def D(N, V, C):
	return 1 / (N - 2) + (1 / np.sqrt(2 * N - 4)) * np.sqrt(2 / (N-2) + (np.log(4 / C) + 2 * V * np.log(N)) ) 



FUN_ARR = [OVC, VVC, RPB, PVB, D]
const_V = 50
const_C = 0.05



def draw(start, end):

	step = int(np.ceil((end - start) / 100))

	pl.figure(0, figsize=(14.0, 10.0))
	n_range = range(start, end, step)

	pl.title('bounds for N from %d to %d' %(start, end))
	for fun in FUN_ARR:
		e_range = [fun(N, const_V, const_C) for N in n_range]
		pl.plot(n_range, e_range, label='$bound-{name}$'.format(name = fun.__name__))

	pl.xlabel("N")
	pl.ylabel("bound")
	pl.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol = 5)


	pl.savefig(("%s/Q4_%d-%d.png") % ("all_output", start, end))
	pl.close()


# range from 3 ~ 20
draw(3, 20)

# range from 100 ~ 1000
draw(100, 1000)

# range from 1,000 ~ 10,000
draw(1000, 10000)

# range from 10,000 ~ 100,000
draw(10000, 100000)