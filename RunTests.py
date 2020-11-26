import OutputTest
import DataTest
import subprocess
import json

#res = subprocess.run(['python3', 'BirthdayProblemClass.py', '366', '-n', '23', '-a'], stdout=subprocess.PIPE)
#print(res.returncode)
#print(res.stdout.decode('utf-8'))

#r = BirthdayProblemCLISolver.solve(['366', '-n', '23', '-a'])
#print(r)

def runTest(testData, resFn, assemblerFn, dividerFn):
	failed = 0
	for i, (args, ans) in enumerate(testData, start = 1):
		print("Test " + str(i) + ": input '" + args + "'")
		error = False
		ansSingle = assemblerFn(ans)
		try:
			resSingle = assemblerFn(resFn(args))
		except BaseException as e:
			error = True
			resSingle = e
		if error or ansSingle != resSingle:
			print("-> failed:")
			if error:
				print("    Due to error: " + str(resSingle))
			else:	
				print("    Expected: " )
				for row in dividerFn(resSingle):
					print("        " + str(row))
				print("    to be equal to: ")
				for row in dividerFn(ansSingle):
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
		["OutputTest", OutputTest.testData, OutputTest.testFn, OutputTest.assemblerFn, OutputTest.dividerFn],
		["DataTest", DataTest.testData, DataTest.testFn, DataTest.assemblerFn, DataTest.dividerFn]
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








