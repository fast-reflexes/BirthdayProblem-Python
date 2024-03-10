from BirthdayProblem import BirthdayProblem

testFn = lambda args: BirthdayProblem.CLISolver.solve(args.split(" "))

assemblerFn = lambda inp: "\n".join(inp) if(isinstance(inp, list)) else inp

dividerFn = lambda inp: inp.split("\n") if(isinstance(inp, str)) else inp

testData = [
	['1 -p 1.0 -a', True,
		[
			'The number of samples, sampled uniformly at random from a set of 1 items, needed to have at least a 100% chance of a non-unique sample is:',
			'          2 (Trivial solution)'
		]
	],
	['1 -p 0.0 -a', True,
		[
			'The number of samples, sampled uniformly at random from a set of 1 items, needed to have at least a 0% chance of a non-unique sample is:',
			'          1 (Trivial solution)'
		]
	],
	['1 -p 0.5 -a', True,
		[
			'The number of samples, sampled uniformly at random from a set of 1 items, needed to have at least a 50% chance of a non-unique sample is:',
			'          2 (Trivial solution)'
		]
	],
	['1000000000 -p 0.0000001 -t', True,
		[
			'The number of samples, sampled uniformly at random from a set of 1000000000 (=10^9) items, needed to have at least a 0.00001% (=10^-7) chance of a non-unique sample is:',
			'          15 (Taylor series approximation used in main calculation)'
		]
	],
	['1 -n 1 -a', True,
		[
			'The probability of finding at least one non-unique sample among 1 samples, sampled uniformly at random from a set of 1 items, is:',
			'          0% (Trivial solution)'
		]
	],
	['1 -n 0 -a', True,
		[
			'The probability of finding at least one non-unique sample among 0 samples, sampled uniformly at random from a set of 1 items, is:',
			'          0% (Trivial solution)'
		]
	],
	['1 -n 2 -a', True,
		[
			'The probability of finding at least one non-unique sample among 2 samples, sampled uniformly at random from a set of 1 items, is:',
			'          100% (Trivial solution)'
		]
	],
	['69 -p 0.5 -a', True,
		[
			'The number of samples, sampled uniformly at random from a set of 69 items, needed to have at least a 50% chance of a non-unique sample is:',
			'          11 (Exact method)',
			'          10 (Taylor series approximation used in main calculation)'
		]
	],
	['83 -p 0.5 -a', True,
		[
			'The number of samples, sampled uniformly at random from a set of 83 items, needed to have at least a 50% chance of a non-unique sample is:',
			'          12 (Exact method)',
			'          11 (Taylor series approximation used in main calculation)'
		]
	],
	['1000000000 -p 0.5 -a', True,
		[
			'The number of samples, sampled uniformly at random from a set of 1000000000 (=10^9) items, needed to have at least a 50% chance of a non-unique sample is:',
			'          37234 (Exact method)',
			'          37233 (Taylor series approximation used in main calculation)'
		]
	],
	['366 -n 23 -a', True,
		[
			'The probability of finding at least one non-unique sample among 23 samples, sampled uniformly at random from a set of 366 items, is:',
			'          ≈50.6323011819% (Exact method)',
			"          ≈50.6315474495% (Stirling's approximation used in factorial calculation)",
			'          ≈51.4549326419% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['366 -p 0.5 -a', True,
		[
			'The number of samples, sampled uniformly at random from a set of 366 items, needed to have at least a 50% chance of a non-unique sample is:',
			'          23 (Exact method)',
			'          23 (Taylor series approximation used in main calculation)'
		]
	],
	['6274264876827642864872634872364782634 -n 2376287346287353638 -s -t', True,
		[
			'The probability of finding at least one non-unique sample among 2376287346287353638 (≈2*10^18) samples, sampled uniformly at random from a set of 6274264876827642864872634872364782634 (≈6*10^36) items, is:',
			"          ≈36.2366927782% (Stirling's approximation used in factorial calculation)",
			'          ≈36.2366927782% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['128 -n 0 -b -s -t', True,
		[
			'The probability of finding at least one non-unique sample among 2^0 samples, sampled uniformly at random from a set of 2^128 items, is:',
			'          0% (Trivial solution)'
		]
	],
	['128 -n 129 -b -s -t', True,
		[
			'The probability of finding at least one non-unique sample among 2^129 samples, sampled uniformly at random from a set of 2^128 items, is:',
			'          100% (Trivial solution)'
		]
	],
	['128 -n 64 -b -s -t', True,
		[
			'The probability of finding at least one non-unique sample among 2^64 samples, sampled uniformly at random from a set of 2^128 items, is:',
			"          ≈39.3469340287% (Stirling's approximation used in factorial calculation)",
			'          ≈39.3469340287% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['128 -p 0.5 -b -t', True,
		[
			'The number of samples, sampled uniformly at random from a set of 2^128 items, needed to have at least a 50% chance of a non-unique sample is:',
			'          ≈2^64.2356168135 (Taylor series approximation used in main calculation)'
		]
	],
	['2000000 -n 1000000 -b -s -t', True,
		[
			'The probability of finding at least one non-unique sample among 2^1000000 samples, sampled uniformly at random from a set of 2^2000000 items, is:',
			"          N/A             (Calculation failed: needed precision for method exceeds maximum precision (Exact method with Stirling's approximation))",
			'          ≈39.3469340287% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['2000000 -p 0.5 -b -t', True,
		[
			'The number of samples, sampled uniformly at random from a set of 2^2000000 items, needed to have at least a 50% chance of a non-unique sample is:',
			'          ≈2^1000000.2356168135 (Taylor series approximation used in main calculation)'
		]
	],
	['8 -n 3 -b -a', True,
		[
			'The probability of finding at least one non-unique sample among 2^3 samples, sampled uniformly at random from a set of 2^8 items, is:',
			'          ≈10.4576930892% (Exact method)',
			"          ≈10.4567528314% (Stirling's approximation used in factorial calculation)",
			'          ≈11.7503097415% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['256 -n 8 -a', True,
		[
			'The probability of finding at least one non-unique sample among 8 samples, sampled uniformly at random from a set of 256 items, is:',
			'          ≈10.4576930892% (Exact method)',
			"          ≈10.4567528314% (Stirling's approximation used in factorial calculation)",
			'          ≈11.7503097415% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['52 -p 0.1 -c -t', True,
		[
			'The number of samples, sampled uniformly at random from a set of 80658175170943878571660636856403766975289505440883277824000000000000 (≈8*10^67) items, needed to have at least a 10% chance of a non-unique sample is:',
			'          4122665867622533660736208120290868 (≈4*10^33) (Taylor series approximation used in main calculation)'
		]
	],
	['52 -p 0.5 -c -t', True,
		[
			'The number of samples, sampled uniformly at random from a set of 80658175170943878571660636856403766975289505440883277824000000000000 (≈8*10^67) items, needed to have at least a 50% chance of a non-unique sample is:',
			'          10574307231100289363611308602026252 (≈10^34) (Taylor series approximation used in main calculation)'
		]
	],
	['52 -n 10000000000000000000 -c -s -t', True,
		[
			'The probability of finding at least one non-unique sample among 10000000000000000000 (=10^19) samples, sampled uniformly at random from a set of 80658175170943878571660636856403766975289505440883277824000000000000 (≈8*10^67) items, is:',
			"          ≈0% (≈6*10^-31) (Stirling's approximation used in factorial calculation)",
			'          ≈0% (≈6*10^-31) (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['52 -n 10000000000000000000000000000000000 -c -s -t', True,
		[
			'The probability of finding at least one non-unique sample among 10000000000000000000000000000000000 (=10^34) samples, sampled uniformly at random from a set of 80658175170943878571660636856403766975289505440883277824000000000000 (≈8*10^67) items, is:',
			"          ≈46.2001746672% (Stirling's approximation used in factorial calculation)",
			'          ≈46.2001746672% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['4 -n 18 -b -c -a', True,
		[
			'The probability of finding at least one non-unique sample among 2^18 samples, sampled uniformly at random from a set of ≈2^44.2501404699 items, is:',
			'          ≈0.1640861961% (≈2*10^-3) (Exact method)',
			"          ≈0.1640861961% (≈2*10^-3) (Stirling's approximation used in factorial calculation)",
			'          ≈0.1640868208% (≈2*10^-3) (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['16 -n 262144 -c -a', True,
		[
			'The probability of finding at least one non-unique sample among 262144 (≈3*10^5) samples, sampled uniformly at random from a set of 20922789888000 (≈2*10^13) items, is:',
			'          ≈0.1640861961% (≈2*10^-3) (Exact method)',
			"          ≈0.1640861961% (≈2*10^-3) (Stirling's approximation used in factorial calculation)",
			'          ≈0.1640868208% (≈2*10^-3) (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['20922789888000 -n 262144 -a', True,
		[
			'The probability of finding at least one non-unique sample among 262144 (≈3*10^5) samples, sampled uniformly at random from a set of 20922789888000 (≈2*10^13) items, is:',
			'          ≈0.1640861961% (≈2*10^-3) (Exact method)',
			"          ≈0.1640861961% (≈2*10^-3) (Stirling's approximation used in factorial calculation)",
			'          ≈0.1640868208% (≈2*10^-3) (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['128 -n 64 -b -c -s -t', True,
		[
			'The probability of finding at least one non-unique sample among 2^64 samples, sampled uniformly at random from a set of ≈2^43065219282621326757565580404980237828911.4871409133 items, is:',
			"          N/A (Calculation failed: d exceeds maximum size and is needed for method (Exact method with Stirling's approximation))",
			'          0%  (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['1280 -n 640 -b -c -s -t', True,
		[
			'The probability of finding at least one non-unique sample among 2^640 samples, sampled uniformly at random from a set of ≈2^26614275474014559821953787196100807012412948367028783328633986189111799719299525295290069853854877867120534538070982737886888824825850066183609939356930416666755910887266773840385877776851876084664629106697034459995685244418266399190317043076208186461319737435225525519543453247219560088300601118286958869004726993677805799134087110255288245085785541666888810491274634074724367056992419344.3330052449 items, is:',
			"          N/A (Calculation failed: d exceeds maximum size and is needed for method (Exact method with Stirling's approximation))",
			'          0%  (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['1280 -p 0.5 -b -c -e', True,
		[
			'The number of samples, sampled uniformly at random from a set of ≈2^26614275474014559821953787196100807012412948367028783328633986189111799719299525295290069853854877867120534538070982737886888824825850066183609939356930416666755910887266773840385877776851876084664629106697034459995685244418266399190317043076208186461319737435225525519543453247219560088300601118286958869004726993677805799134087110255288245085785541666888810491274634074724367056992419344.3330052449 items, needed to have at least a 50% chance of a non-unique sample is:',
			"          N/A (Calculation failed: d exceeds maximum size and is needed for method (Exact method))"
		]
	 ],
	['12800 -n 6400 -b -c -s -t', False, "dLog exceeds maximum size and is needed to initialize calculations"]
]







