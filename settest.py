import sys
import re
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import random

def set_cover(universe, subsets, num_subsets, cost, sigval, sigstr, n):
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
		max_importance = calc_importance(subsets, covered.difference(universe),
									cost, sigval, sigstr, n);
#		subset = max(subsets, key=lambda s: len(s - covered));
		subset = subsets[max_importance]
		subsets.remove(subsets[max_importance]);
		cover.append(subset);
		covered |= subset;

		if i > 0:
			overlap = subset.intersection(covered);

	if elements == covered:
 		return cover, overlap, 1;
	else:
		return universe.difference(covered), overlap, 0;

def calc_importance(subsets, uncovered, cost, sigval, sigstr, n):
	importance = [0] * n * n;
	index = 0;
	max_importance = 0;

	for x in subsets:
		new_covers = x.intersection(uncovered);
		if len(new_covers) == 0:
			index += 1;
			continue;

		cover_val = int((len(new_covers)/len(uncovered))*100);
		importance[index] = cover_val + cost[index] + sigval[index] + sigstr[index];

		if importance[index] > max_importance:
			max_importance = index;

		index += 1;

	return max_importance;
 
def get_sets_from_file(filename):
	fp = open(filename, "r");
	subsets = [];
	tmp = [];

	n = int(fp.readline());

	for line in fp:
		line = line.rstrip();
		tmp = line.split(', ');
		s = set();

		if filename == "covered.csv" or filename == "sigstr.csv" :
			for i in range(n*n):
				if int(tmp[i]):
					s.add(int(i));
		subsets.append(s);
		if filename == "cost.csv" or filename == "sigval.csv":
			subsets = tmp;

	fp.close();

	return subsets, n;

def plot_heatmap(cover, overlap, covered, n):
	data = [[1]*n for _ in range(n)];

	if covered == 0:
		for x in cover:
			data[x//n][x%n] = 0.5;

#	for x in overlap:
#			data[x//n][x%n] = 0;

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
	num_subsets = int(sys.argv[1]);

	s, n = get_sets_from_file("covered.csv");
	sigstr, n = get_sets_from_file("sigstr.csv");
	sigval, n = get_sets_from_file("sigval.csv");
	cost, n = get_sets_from_file("cost.csv");

	universe = set(range(0, n*n));
	cover, overlap, covered = set_cover(universe, s, num_subsets, 
										cost, sigval, sigstr, n);

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
