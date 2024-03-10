import TextTest
import JsonTest
import LibraryTest
from BirthdayProblem import SolverException
import subprocess
import json

#res = subprocess.run(['python3', 'BirthdayProblemClass.py', '366', '-n', '23', '-a'], stdout=subprocess.PIPE)
#print(res.returncode)
#print(res.stdout.decode('utf-8'))

#r = BirthdayProblemCLISolver.solve(['366', '-n', '23', '-a'])
#print(r)

'''
resFn is the function that actually does the calculation. Assembler function assembles the assumed answer to its output
form (if needed) and dividerFn is the inversion of the assemblerFn; it divides the output of the resFn into someting 
that is simpler to show in the test output (also here only if needed).
'''
def runTest(testData, resFn, assemblerFn, dividerFn):
	failed = 0
	for i, (args, shouldTestSucceed, ans) in enumerate(testData, start = 1):
		print("Test " + str(i) + ": input '" + str(args) + "'")
		error = False
		ansSingle = assemblerFn(ans) if shouldTestSucceed else ans
		try:
			resSingle = assemblerFn(resFn(args))
		except BaseException as e:
			error = True
			resSingle = str(e)
		if (shouldTestSucceed and (error or ansSingle != resSingle)) or (not shouldTestSucceed and (not error or ansSingle != resSingle)):
			print("-> failed:")
			if(shouldTestSucceed):
				if(error):
					print("    Due to error: " + str(resSingle))
				else:
					print("    Expected: " )
					for row in dividerFn(resSingle):
						print("        " + str(row))
					print("    to be equal to: ")
					for row in dividerFn(ansSingle):
						print("        " + str(row))
			else:
				if(error):
					print("    Expected exception message: '" + resSingle + "'")
					print("    to be equal to exception message: '" + ansSingle + "'")
				else:
					print("    Due to error: test should have failed but was successful with output ...")
					for row in dividerFn(resSingle):
						print("        " + str(row))
			failed += 1
		else:
			print("-> succeeded")
	print("========")
	if failed > 0:
		print("Summary: " + str(failed) + " tests failed")
		print()
	else:
		print("Summary: all " + str(len(testData)) + " tests succeeded")

	return failed

if __name__ == '__main__':
	failed = 0
	print("Running all tests...")
	print()
	tests = [
		["TextTest", TextTest.testData, TextTest.testFn, TextTest.assemblerFn, TextTest.dividerFn],
		["JsonTest", JsonTest.testData, JsonTest.testFn, JsonTest.assemblerFn, JsonTest.dividerFn],
		["LibraryTest", LibraryTest.testData, LibraryTest.testFn, LibraryTest.assemblerFn, LibraryTest.dividerFn]
	]
	for (testName, testData, testFn, assemblerFn, dividerFn) in tests:
		print("-> Running '" + testName + "'")
		print("========")
		failed += runTest(testData, testFn, assemblerFn, dividerFn)
		print("========")
		print()
	print("================")
	if failed > 0:
		print("Test suite had " + str(failed) + " failing tests in total")
	else:
		print("Test suite successful!")
	print()








