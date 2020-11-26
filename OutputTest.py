from BirthdayProblem import BirthdayProblem
import subprocess
import json

testFn = lambda args: BirthdayProblem.CLISolver.solve(args.split(" "))

assemblerFn = lambda inp: inp if(isinstance(inp, str)) else "\n".join(inp)

dividerFn = lambda inp: inp.split("\n") if(isinstance(inp, str)) else inp

testData = [
	['1 -p 1.0 -a', 
		[
			'The number of samples, sampled uniformly at random from a set of 1 items, needed to have at least a 100% chance of a non-unique sample is:',
			'          2 (Trivial solution)'
		]
	],
	['1 -p 0.0 -a',
		[
			'The number of samples, sampled uniformly at random from a set of 1 items, needed to have at least a 0% chance of a non-unique sample is:',
			'          1 (Trivial solution)'
		]
	],
	['1 -p 0.5 -a',
		[
			'The number of samples, sampled uniformly at random from a set of 1 items, needed to have at least a 50% chance of a non-unique sample is:',
			'          2 (Taylor series approximation used in main calculation)'
		]
	],
	['1000000000 -p 0.0000001',
		[
			'The number of samples, sampled uniformly at random from a set of 1000000000 (=10^9) items, needed to have at least a 0.00001% (=10^-7) chance of a non-unique sample is:',
			'          15 (Taylor series approximation used in main calculation)'
		]
	],
	['1 -n 1 -a',
		[
			'The probability of finding at least one non-unique sample among 1 samples, sampled uniformly at random from a set of 1 items, is:',
			'          0% (Trivial solution)'
		]
	],
	['1 -n 0 -a',
		[
			'The probability of finding at least one non-unique sample among 0 samples, sampled uniformly at random from a set of 1 items, is:',
			'          0% (Trivial solution)'
		]
	],
	['1 -n 2 -a',
		[
			'The probability of finding at least one non-unique sample among 2 samples, sampled uniformly at random from a set of 1 items, is:',
			'          100% (Trivial solution)'
		]
	],
	['366 -n 23 -a',
		[
			'The probability of finding at least one non-unique sample among 23 samples, sampled uniformly at random from a set of 366 items, is:',
			'          ≈50.6323011819% (Exact method)',
			"          ≈50.6315474495% (Stirling's approximation used in factorial calculation)",
			'          ≈51.4549326419% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['366 -p 0.5',
		[
			'The number of samples, sampled uniformly at random from a set of 366 items, needed to have at least a 50% chance of a non-unique sample is:',
			'          23 (Taylor series approximation used in main calculation)'
		]
	],
	['6274264876827642864872634872364782634 -n 2376287346287353638 -s -t',
		[
			'The probability of finding at least one non-unique sample among 2376287346287353638 (≈2*10^18) samples, sampled uniformly at random from a set of 6274264876827642864872634872364782634 (≈6*10^36) items, is:',
			"          ≈36.2366927782% (Stirling's approximation used in factorial calculation)",
			'          ≈36.2366927782% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['128 -n 0 -b -s -t',
		[
			'The probability of finding at least one non-unique sample among 2^0 samples, sampled uniformly at random from a set of 2^128 items, is:',
			'          0% (Trivial solution)'
		]
	],
	['128 -n 129 -b -s -t',
		[
			'The probability of finding at least one non-unique sample among 2^129 samples, sampled uniformly at random from a set of 2^128 items, is:',
			'          100% (Trivial solution)'
		]
	],
	['128 -n 64 -b -s -t',
		[
			'The probability of finding at least one non-unique sample among 2^64 samples, sampled uniformly at random from a set of 2^128 items, is:',
			"          ≈39.3469340287% (Stirling's approximation used in factorial calculation)",
			'          ≈39.3469340287% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['128 -p 0.5 -b',
		[
			'The number of samples, sampled uniformly at random from a set of 2^128 items, needed to have at least a 50% chance of a non-unique sample is:',
			'          ≈2^64.2356168135 (Taylor series approximation used in main calculation)'
		]
	],
	['2000000 -n 1000000 -b -s -t',
		[
			'The probability of finding at least one non-unique sample among 2^1000000 samples, sampled uniformly at random from a set of 2^2000000 items, is:',
			"          N/A             (Calculation failed with this method (Exact method with Stirling's approximation))",
			'          ≈39.3469340287% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['2000000 -p 0.5 -b',
		[
			'The number of samples, sampled uniformly at random from a set of 2^2000000 items, needed to have at least a 50% chance of a non-unique sample is:',
			'          ≈2^1000000.2356168135 (Taylor series approximation used in main calculation)'
		]
	],
	['8 -n 3 -b -a',
		[
			'The probability of finding at least one non-unique sample among 2^3 samples, sampled uniformly at random from a set of 2^8 items, is:',
			'          ≈10.4576930892% (Exact method)',
			"          ≈10.4567528314% (Stirling's approximation used in factorial calculation)",
			'          ≈11.7503097415% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['256 -n 8 -a',
		[
			'The probability of finding at least one non-unique sample among 8 samples, sampled uniformly at random from a set of 256 items, is:',
			'          ≈10.4576930892% (Exact method)',
			"          ≈10.4567528314% (Stirling's approximation used in factorial calculation)",
			'          ≈11.7503097415% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['52 -p 0.1 -c',
		[
			'The number of samples, sampled uniformly at random from a set of ≈80529020383886612857810199580012764961409004334781435987268084328737 (≈8*10^67) items, needed to have at least a 10% chance of a non-unique sample is:',
			'          4119363813276486714957808853108064 (≈4*10^33) (Taylor series approximation used in main calculation)'
		]
	],
	['52 -p 0.5 -c',
		[
			'The number of samples, sampled uniformly at random from a set of ≈80529020383886612857810199580012764961409004334781435987268084328737 (≈8*10^67) items, needed to have at least a 50% chance of a non-unique sample is:',
			'          10565837726592754214318243269428637 (≈10^34) (Taylor series approximation used in main calculation)'
		]
	],
	['52 -n 10000000000000000000 -c -s -t',
		[
			'The probability of finding at least one non-unique sample among 10000000000000000000 (=10^19) samples, sampled uniformly at random from a set of ≈80529020383886612857810199580012764961409004334781435987268084328737 (≈8*10^67) items, is:',
			"          ≈0% (≈6*10^-31) (Stirling's approximation used in factorial calculation)",
			'          ≈0% (≈6*10^-31) (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['52 -n 10000000000000000000000000000000000 -c -s -t',
		[
			'The probability of finding at least one non-unique sample among 10000000000000000000000000000000000 (=10^34) samples, sampled uniformly at random from a set of ≈80529020383886612857810199580012764961409004334781435987268084328737 (≈8*10^67) items, is:',
			"          ≈46.2536366051% (Stirling's approximation used in factorial calculation)",
			'          ≈46.2536366051% (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['4 -n 18 -b -c -a',
		[
			'The probability of finding at least one non-unique sample among 2^18 samples, sampled uniformly at random from a set of ≈2^44.2426274105 items, is:',
			'          ≈0.1649423866% (≈2*10^-3) (Exact method)',
			"          ≈0.1649422224% (≈2*10^-3) (Stirling's approximation used in factorial calculation)",
			'          ≈0.1649428504% (≈2*10^-3) (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['16 -n 262144 -c -a',
		[
			'The probability of finding at least one non-unique sample among 262144 (≈3*10^5) samples, sampled uniformly at random from a set of ≈20814114415223 (≈2*10^13) items, is:',
			'          ≈0.1649423866% (≈2*10^-3) (Exact method)',
			"          ≈0.1649422224% (≈2*10^-3) (Stirling's approximation used in factorial calculation)",
			'          ≈0.1649428504% (≈2*10^-3) (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['20922789888000 -n 262144 -a',
		[
			'The probability of finding at least one non-unique sample among 262144 (≈3*10^5) samples, sampled uniformly at random from a set of 20922789888000 (≈2*10^13) items, is:',
			'          ≈0.1640861961% (≈2*10^-3) (Exact method)',
			"          ≈0.1640861961% (≈2*10^-3) (Stirling's approximation used in factorial calculation)",
			'          ≈0.1640868208% (≈2*10^-3) (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['128 -n 64 -b -c -s -t',
		[
			'The probability of finding at least one non-unique sample among 2^64 samples, sampled uniformly at random from a set of ≈2^43065219282621326757565580404980237828911.4871409133 items, is:',
			"          N/A (Calculation failed with this method (Exact method with Stirling's approximation))",
			'          0%  (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['1280 -n 640 -b -c -s -t',
		[
			'The probability of finding at least one non-unique sample among 2^640 samples, sampled uniformly at random from a set of ≈2^26614275474014559821953787196100807012412948367028783328633986189111799719299525295290069853854877867120534538070982737886888824825850066183609939356930416666755910887266773840385877776851876084664629106697034459995685244418266399190317043076208186461319737435225525519543453247219560088300601118286958869004726993677805799134087110255288245085785541666888810491274634074724367056992419344.3330052449 items, is:',
			"          N/A (Calculation failed with this method (Exact method with Stirling's approximation))",
			'          0%  (Taylor series approximation used in main calculation (removes need for factorial calculation))'
		]
	],
	['12800 -n 6400 -b -c -s -t',
		[
			'The probability of finding at least one non-unique sample among 2^6400 samples, sampled uniformly at random from a set of 2^195481434018629685778487103146708500752736213064718676249545151022045397482857597428481127234222047957323538558765759046381848848063455663519719797989351815535175457085989203721784032464876849620281679432018404279226476939259867255841274689492954742994284006449483868578632835566315781171432272849009642468454018314789246759341533296212438556574379745571168608824067975240422258923055944076152529559912823909309124810985532884360261662285062836424865351039206945716054362798713336122732087662369880089163325248832153675247421823718016726409856359650067095105775921431164409410437467946244428601232254783255383056006365975975425665355754321280933248235706181191807957992935411915548982601074393898274391664685426876716154860477856779473223374023978925142485495476478087813339087382767116635902576699942258294621936398726755762706650775703182209143584561871887824759287240821975266649257107795548071419814632899561764612755000667569934752523833991820915389865648044177084195760591750088527916935573858800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 items, is:',
			"          N/A (Calculation failed with this method (Exact method with Stirling's approximation))",
			'          N/A (Calculation failed with this method (Taylor approximation))'
		]
	]	
]







