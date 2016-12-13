import os
import sys, getopt
import hw1problems


def usage():
	print("execute: \n\tpython main.py -p pid -f fun [-o output] [-v]")
	print("or")
	print("\tpython main.py -a [-o output] [-v]")
	print("\t-p[--problem]:  pid should range from 15 to 20")
	print("\t-f[--function]: fun should be either `exp` or `dig` without `dig` with -p 15")
	print("\t-o[--output]: output folder")
	print("\t-a: do_all")


def solve_all(config):

	pMap = hw1problems.PROBLEM_ALGORITHM_MAP
	for pid in pMap:
		for op in pMap[pid]:
			solve_problem({
				"output": config["output"],
				"verbose": config["verbose"],
				"problem": pid,
				"function": op
			})


def solve_problem(config):

	output_dir = config["output"]
	output_dir = os.path.join(os.path.dirname(__file__), output_dir)


	pid = config["problem"]
	op = config["function"]
	verbose = config["verbose"]


	funConfig = hw1problems.PROBLEM_ALGORITHM_MAP[pid][op]
	dataConfig = hw1problems.PROBLEM_DATASET_MAP[pid]


	if not "times" in config:
		config["times"] = funConfig["default_times"]

	times = config["times"]
		


	training_path = os.path.join(os.path.dirname(__file__), dataConfig["training_path"])
	test_path = os.path.join(os.path.dirname(__file__), dataConfig["test_path"])


	hw1problems.ini_problem(training_path, test_path, output_dir, "exp_records.db")


	for x in range(0,times):
		if verbose:
			print("-------->executing problem-%s-%s at NO.%d-time" %(pid, op, x+1))
		hw1problems.execute(funConfig["fun"], funConfig["parameters"])


def main():

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:f:o:t:a", ["help", "problem", "function", "output", "times"])
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)

	config = {
		"output": "all_output",
		"verbose": False
	}

	for o, a in opts:

		if o == "-v":
			config["verbose"] = True

		elif o == "-a":
			config["all"] = True

		elif o in ("-h", "--help"):
			usage()
			sys.exit(2)

		elif o in ("-t", "--times"):
			config["times"] = a

		# which problem
		elif o in ("-p", "--problem"):
			config["problem"] = a

		# run alg or plot
		elif o in ("-f", "--function"):
			config["function"] = a

		# test output path
		elif o in ("-o", "--output"):
			config["output"] = a

		else:
			assert False, "unhandled option"

	if "all" in config and config["all"]:
		solve_all(config)
	else:
		try:
			solve_problem(config)
		except (IndexError, KeyError) as e:
			print("Cannot find parameter", e)
			usage()
			sys.exit(2)

if __name__ == '__main__':
	main()
