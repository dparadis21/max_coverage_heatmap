import sys
import re
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import random

def set_cover(universe, subsets, num_subsets):
	"""Find a family of subsets that covers the universal set"""
	overlap = set();
	elements = set(e for s in subsets for e in s)

	# Check the subsets cover the universe
	if elements != universe:
		cover = universe.difference(elements);
		return cover, overlap, 0;

	covered = set();
	cover = [];

	# Greedily add the subsets with the most uncovered points
	for i in range(num_subsets):
		if covered == elements:
			break;
		subset = max(subsets, key=lambda s: len(s - covered));
		cover.append(subset);
		covered |= subset;

		if i > 0:
			overlap = subset.intersection(covered);

	if elements == covered:
 		return cover, overlap, 1;
	else:
		return universe.difference(covered), overlap, 0;
 
def get_sets_from_file():
	fp = open(sys.argv[1], "r");
	subsets = [];
	tmp = [];

	n = int(fp.readline());

	for line in fp:
		line = line.rstrip();
		tmp = line.split(', ');
		s = set();

		for i in range(n*n):
			if int(tmp[i]):
				s.add(int(i));

		subsets.append(s);
	fp.close();

	return subsets, n;

def plot_heatmap(cover, overlap, covered, n):
	data = [[1]*n for _ in range(n)];

	if covered == 0:
		for x in cover:
			data[x//n][x%n] = 0.5;

	for x in overlap:
			data[x//n][x%n] = 0;

	ax = sns.heatmap(data, vmin = 0, vmax = 1, linewidths = 1, cbar = False, cmap='brg');
	plt.show();

def choose_subsets(num_subsets, s, n):
	subset_indeces = set();
	subsets = [];
	while len(subset_indeces) < int(sys.argv[2]):
		subset_indeces.add(random.randint(0, n*n - 1));

	subset_indeces = list(subset_indeces);

	for x in range(len(subset_indeces)):
		subsets.append(s[subset_indeces[x]]);

	return subsets;


def main():
	best_cover = 0;
	covered = 0;
	num_subsets = int(sys.argv[2]);
	s, n = get_sets_from_file();
	universe = set(range(0, n*n));
	cover, overlap, covered = set_cover(universe, s, num_subsets);

#	while covered == 0:
#		subsets = choose_subsets(sys.argv[2], s, n);
#		cover, overlap, covered = set_cover(universe, subsets);
	
#		if covered:
#			break;

#		if len(cover) > best_cover:
#			best_cover = len(cover);

	if covered:
		print "Overlap";
		print list(overlap);

		print "Covered";
		print "Number of sets: " + str(len(cover));
		for x in cover:
			print list(x);
	else:
		print "Uncovered";
		print list(cover);

		print "Overlap";
		print list(overlap);

	plot_heatmap(cover, overlap, covered, n);

main();
