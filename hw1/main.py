import os
import sys, getopt
import hw1problems


def usage():
	print("execute: \n\tpython main.py -p pid -f fun [-o output] [-v]")
	print("or")
	print("python main.py -a [-o output] [-v]")
	print("\t-p[--problem]:  pid should range from 15 to 20")
	print("\t-f[--function]: fun should be either `exp` or `dig`")
	print("\t-o[--output]: output folder")
	print("\t-v: to log verbose")
	print("\t-a: do_all")


def solve_all(config):

	output_dir = config["output"] if  "output" in config else "all_outputs"
	verbose = config["verbose"] if  "verbose" in config else False

	for pid in hw1problems.PROBLEM_ALGORITHM_MAP:
		problem = hw1problems.PROBLEM_ALGORITHM_MAP[pid]
		for op in ["exp", "dig"]:
			solve_problem({
				"output": output_dir,
				"problem": pid,
				"function": op,
				"verbose": verbose
			})


def solve_problem(config):

	output_dir = config["output"] if  "output" in config else "output"
	verbose = config["verbose"] if "verbose" in config else False

	output_dir = os.path.join(os.path.dirname(__file__), output_dir)

	pid = config["problem"]
	op = config["function"]


	if "times" in config:
		times = config["times"]
	elif op == "dig":
		times = 1
	elif pid == "15":
		times = config["times"] if "times" in config else 1
	else:
		times = config["times"] if "times" in config else 2



	t = hw1problems.PROBLEM_ALGORITHM_MAP[pid][op]

	training_path = os.path.join(os.path.dirname(__file__), hw1problems.PROBLEM_DATASET_MAP[pid]["training_path"])
	test_path = os.path.join(os.path.dirname(__file__), hw1problems.PROBLEM_DATASET_MAP[pid]["test_path"])


	hw1problems.ini_problem(training_path, test_path, output_dir, "exp_records.db")


	for x in range(0,times):
		if verbose:
			print("-------->executing problem-%s-%s at NO.%d-time" %(pid, op, x+1))
		hw1problems.execute(t[0], t[1])


def main():

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:f:o:av", ["help", "problem", "function", "output"])
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)

	config = dict()

	for o, a in opts:

		if o == "-v":
			config["verbose"] = True

		elif o == "-a":
			config["all"] = True

		elif o in ("-h", "--help"):
			usage()
			sys.exit(2)
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
		if( not "problem" in config) or (not config["problem"] in hw1problems.PROBLEM_DATASET_MAP):
			print("problem index wrong!")
			usage()
			sys.exit(2)

		if (not "function" in config) or not (config["function"] == "exp" or config["function"] == "dig"):
			print("function is necessary!")
			usage()
			sys.exit(2)


		solve_problem(config)

if __name__ == '__main__':
	main()
