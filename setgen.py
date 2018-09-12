import sys
import random

n = int(sys.argv[1]); # number of elements in the set that needs to be covered
sig_cutoff = 20; # signal strength


def main():
	print n;

	for i in range(n*n):
		signals = random_sig();

		for j in range(n*n):
			if j != n*n - 1:
				print str(signals[j]) + ',',;
			else:
				print str(signals[j]),;

		#	if j % n == n - 1:
		#		print;
		print;

def random_sig():
	s = [0] * n * n;
	for i in range(n*n):
		r = random.randint(0, 100);
		if (r < sig_cutoff):
			s[i] = 1;
		else:
			s[i] = 0;

	return s;

def calc_sig_str(location):
	signals = [0] * n * n;
	location_row = location // n;
	location_col = location % n;

	for i in range(n*n):
		point_row = i // n;
		point_col = i % n;
		hori_diff = abs(point_col - location_col);
		vert_diff = abs(point_row - location_row);

		if hori_diff > vert_diff:
			if vert_diff == 0:
				distance = hori_diff;
			else:
				distance = vert_diff
		else:
			if hori_diff == 0:
				distance = vert_diff;
			else:
				distance = hori_diff;

		if i == location:
			s = sig_cutoff + 1;
		else:
			s = random.randint(0, n - distance);

		if s > sig_cutoff:
			signals[i] = 1;
		else:
			signals[i] = 0;

	return signals;

def is_connected(signals, origin, connected):

	for i in range(n*n):
		isolated = 0;
		adjacent = [signals[i-n-1], signals[i-n], signals[i-n+1],
					signals[i-1], signals[i+1],
					signals[i+n-1], signals[i+n], signals[i+n+1]];

main();
