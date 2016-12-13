import main
import sys



def test_problem_15():
	print("test_problem_15")
	sys.argv[1:] = ['-p', '15', '-f', 'exp']
	main.main()

def test_problem_16():
	print("test_problem_16")
	sys.argv[1:] = ['-p', '16', '-f', 'exp']
	main.main()
	sys.argv[1:] = ['-p', '16', '-f', 'dig']
	main.main()

def test_problem_17():
	print("test_problem_17")
	sys.argv[1:] = ['-p', '17', '-f', 'exp']
	main.main()
	sys.argv[1:] = ['-p', '17', '-f', 'dig']
	main.main()

def test_problem_18():
	print("test_problem_18")
	sys.argv[1:] = ['-p', '18', '-f', 'exp']
	main.main()
	sys.argv[1:] = ['-p', '18', '-f', 'dig']
	main.main()

def test_problem_19():
	print("test_problem_19")
	sys.argv[1:] = ['-p', '19', '-f', 'exp']
	main.main()
	sys.argv[1:] = ['-p', '19', '-f', 'dig']
	main.main()

def test_problem_20():
	print("test_problem_20")
	sys.argv[1:] = ['-p', '20', '-f', 'exp']
	main.main()
	sys.argv[1:] = ['-p', '20', '-f', 'dig']
	main.main()

test_problem_15()
test_problem_16()
test_problem_17()
test_problem_18()
test_problem_19()
test_problem_20()