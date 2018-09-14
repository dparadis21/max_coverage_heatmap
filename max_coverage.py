import sys
import re
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import random

def set_cover(universe, subsets, num_subsets, cost, sigval, sigstr, n):
	total_cost = 0;
	total_sigval = 0;
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
		max_importance, total_sigval = calc_importance(subsets, covered,
									cost, sigval, sigstr, n, total_sigval);
		subset = subsets[max_importance];
		total_cost += int(cost[max_importance]);

		subsets.remove(subsets[max_importance]);
		cost.remove(cost[max_importance]);

		cover.append(subset);
		covered |= subset;

		if i > 0:
			overlap = subset.intersection(covered);

	if elements == covered:
 		return cover, overlap, 1, total_cost, total_sigval;
	else:
		return universe.difference(covered), overlap, 0, total_cost, total_sigval;

def calc_importance(subsets, covered, cost, sigval, sigstr, n, total_sigval):
	importance = 0;
	max_importance = 0;
	importance_index = 0;
	index = 0;
	sigval_val = 0;

	# TODO add sigstr to weighting.  Need to sum all elements in each set
	# and return an array of sums

	for x in subsets:
		for z in (x - covered):
			sigval_val += int(sigval[z]);

		cover_val = len(x - covered)*n;
		cost_val = n*n - int(cost[index]);

		importance = cover_val + cost_val*0 + sigval_val*0;

		if importance > max_importance:
			max_importance = importance;
			importance_index = index;

		index += 1;

	for x in subsets[importance_index]:
		total_sigval += int(sigval[x]);
		sigval[x] = 0;

	return importance_index, total_sigval;
 
def get_sets_from_file(filename):
	fp = open(filename, "r");
	subsets = [];
	tmp = [];
	sigstr = [];

	n = int(fp.readline());

	for line in fp:
		line = line.rstrip();
		tmp = line.split(', ');
		s = set();

		if filename == "sigstr.csv":
			sigstr.append(tmp);

		if filename == "covered.csv":
			for i in range(n*n):
				if int(tmp[i]):
					s.add(int(i));
		subsets.append(s);
		if filename == "cost.csv" or filename == "sigval.csv":
			subsets = tmp;

	fp.close();

	if filename == "sigstr.csv":
		return sigstr, n;
	else:
		return subsets, n;

def plot_coverage(cover, overlap, covered, best_signals, n):
	data = [[1]*n for _ in range(n)];

	for i in range(n):
		for j in range(n):
			data[i][j] = int(best_signals[i*n + j]);

	ax = sns.heatmap(data, vmin=0, vmax=n*n, annot=True, linewidths = 1,  cmap='Greens');
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
	total_value = 0;
	total_cost = 0;
	cover_value = 0;
	potential_value = 0;
	potential_cost = 0;
	num_subsets = int(sys.argv[1]);

	s, n = get_sets_from_file("covered.csv");
	sigstr, n = get_sets_from_file("sigstr.csv");
	sigval, n = get_sets_from_file("sigval.csv");
	cost, n = get_sets_from_file("cost.csv");
	best_signals = [0] * n * n;

	for i in range(n*n):
		potential_value += int(sigval[i]);
		potential_cost += int(cost[i]);

	universe = set(range(0, n*n));
	cover, overlap, covered, total_cost, total_value = set_cover(universe, s, num_subsets												, cost, sigval, sigstr, n);

	

	cost_efficacy = str(float(1 - float(total_cost)/float(potential_cost))*100) + "%";
	value_efficacy = str(float(float(total_value)/float(potential_value))*100) + "%";
	
	sets, n = get_sets_from_file("covered.csv");

	for i in range(n*n):
		for x in range(len(cover)):
			if sets[i] == cover[x]:
				for j in range(n*n):
					if best_signals[j] < int(sigstr[i][j]):
						best_signals[j] = int(sigstr[i][j]);

	if covered:
		print "Cost";
		print total_cost;
		print "Potential Cost";
		print potential_cost;
		print "Cost Efficacy";
		print cost_efficacy;

		print "Value"
		print total_value;
		print "Potential Value"
		print potential_value;
		print "Value Efficacy";
		print value_efficacy;

		print "Overlap";
		print list(overlap);

		print "Covered";
		print "Number of sets: " + str(len(cover));

		for x in cover:
			print list(x);
	else:
		print "Cost";
		print total_cost;
		print "Potential Cost";
		print potential_cost;
		print "Cost Efficacy";
		print cost_efficacy;

		print "Value"
		print total_value;
		print "Potential Value"
		print potential_value;
		print "Value Efficacy";
		print value_efficacy;

		print "Uncovered";
		print list(cover);

		print "Overlap";
		print list(overlap);

	plot_coverage(cover, overlap, covered, best_signals, n);

main();
