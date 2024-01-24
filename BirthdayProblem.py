from decimal import *
import argparse
from enum import Enum, IntEnum
import re
import sys
import json
import traceback

class SolverException(Exception):

	def __init__(self, code, method = None, message = "(no message available)"):
		self.code = code
		self.method = method
		self.message = message

	def __str__(self):
		methodText = _BirthdayProblemTextFormatter.methodToText(self.method) if self.method is not None else "(method not available)"
		messages = {
			SolverErrorCode.D_NOT_CALCULATED: "d exceeds maximum size and is needed to initialize calculations",
			SolverErrorCode.DLOG_NOT_CALCULATED: "dLog exceeds maximum size and is needed to initialize calculations",
			SolverErrorCode.D_NEEDED_FOR_METHOD: "d exceeds maximum size and is needed for method",
			SolverErrorCode.DLOG_NEEDED_FOR_METHOD: "dLog exceeds maximum size and is needed for method",
			SolverErrorCode.TOO_HIGH_PRECISION: "needed precision for method exceeds maximum precision",
			SolverErrorCode.BAD_INPUT: "bad input: " + self.message
		}
		return messages.get(self.code, "an unknown error was encountered for the " + methodText + " method with code " + str(self.code))



class SolverErrorCode(IntEnum):
	UNKNOWN_ERROR = 1,
	BAD_INPUT = 2,
	DLOG_NOT_CALCULATED = 3,
	D_NOT_CALCULATED = 4,
	D_NEEDED_FOR_METHOD = 5,
	DLOG_NEEDED_FOR_METHOD = 6,
	TOO_HIGH_PRECISION = 7,

class _DecimalContext:

	MAX_PRECISION = 1000
	DECIMAL_PRECISION = 100
	ctx = Context(prec = MAX_PRECISION, rounding = ROUND_HALF_UP)

	@staticmethod
	def reset():
		_DecimalContext.ctx.prec = _DecimalContext.MAX_PRECISION

	@staticmethod
	def isTooPrecise():
		return _DecimalContext.ctx.prec > _DecimalContext.MAX_PRECISION

	@staticmethod
	def adjustPrecision(integerPartSz):
		_DecimalContext.ctx.prec = ((integerPartSz + 1) if(integerPartSz > 0) else 1) + _DecimalContext.DECIMAL_PRECISION

class _DecimalFns:

	########################################################################################################################################################################################################
	########################################################################################################################################################################################################
	#																																																	   #
	#	General calculation methods                 																										         									   #
	#																																																	   #
	########################################################################################################################################################################################################
	########################################################################################################################################################################################################

	# basic constants
	ZERO = Decimal("0")
	HALF = Decimal("0.5")
	ONE = Decimal("1")
	TWO = Decimal("2")
	TEN = Decimal("10")
	HUNDRED = Decimal("100")

	# hard-coded constants with 100 / 1000 decimal precision
	PI_100 = Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')
	PI_1000 = Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989')
	E_100 =  Decimal('2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274')
	E_1000 =  Decimal('2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274274663919320030599218174135966290435729003342952605956307381323286279434907632338298807531952510190115738341879307021540891499348841675092447614606680822648001684774118537423454424371075390777449920695517027618386062613313845830007520449338265602976067371132007093287091274437470472306969772093101416928368190255151086574637721112523897844250569536967707854499699679468644549059879316368892300987931277361782154249992295763514822082698951936680331825288693984964651058209392398294887933203625094431173012381970684161403970198376793206832823764648042953118023287825098194558153017567173613320698112509961818815930416903515988885193458072738667385894228792284998920868058257492796104841984443634632449684875602336248270419786232090021609902353043699418491463140934317381436405462531520961836908887070167683964243781405927145635490613031072085103837505101157477041718986106873969655212671546889570350354')
	PI = PI_1000
	E = E_1000

	# e base and 2 base logarithms of 2 and PI for repeatedly used values and logarithm base conversions
	LOG_E_2 = _DecimalContext.ctx.ln(TWO)
	LOG_E_PI = _DecimalContext.ctx.ln(PI)
	LOG_2_E = _DecimalContext.ctx.divide(ONE, LOG_E_2)
	LOG_2_PI = _DecimalContext.ctx.divide(LOG_E_PI, LOG_E_2)

	@staticmethod
	def isLessThan(a, b):
		return _DecimalContext.ctx.compare(a, b) == Decimal('-1')

	@staticmethod
	def isGreaterThan(a, b):
		return _DecimalContext.ctx.compare(a, b) == _DecimalFns.ONE

	@staticmethod
	def areEqual(a, b):
		return _DecimalContext.ctx.compare(a, b) == _DecimalFns.ZERO

	@staticmethod
	def areNotEqual(a, b):
		return not _DecimalFns.areEqual(a, b)

	@staticmethod
	def isZero(a):
		return a.is_zero()

	@staticmethod
	def isOne(a):
		return _DecimalFns.areEqual(a, _DecimalFns.ONE)

	@staticmethod
	def isNotOne(a):
		return _DecimalFns.areNotEqual(a, _DecimalFns.ONE)

	@staticmethod
	def isGreaterThanOne(a):
		return _DecimalFns.isGreaterThan(a, _DecimalFns.ONE)

	@staticmethod
	def isLessThanOne(a):
		return _DecimalFns.isLessThan(a, _DecimalFns.ONE)

	@staticmethod
	def isGreaterThanZero(a):
		return _DecimalFns.isGreaterThan(a, _DecimalFns.ZERO)

	@staticmethod
	def isLessThanZero(a):
		return _DecimalFns.isLessThan(a, _DecimalFns.ZERO)

	@staticmethod
	def isInteger(a):
		return _DecimalFns.areEqual(a, a.to_integral_value())

	@staticmethod
	def toPercent(p):
		return _DecimalContext.ctx.multiply(p, _DecimalFns.HUNDRED)

	'''
		facultyNTakeM calculates (n)_m = n! / (n - m)!. This can be done naively by calculating (n)_m directly or by first calculating n! and then dividing it by (n - m)!. 
		In log space, that's equal to log(n! / (n - m)!) = log(n!) - log((n - m)!)
	'''
	# input in natural numbers, output in natural logarithms. Not suitable for large m! n! can be calculated naively by using n = m
	@staticmethod
	def facultyNTakeMNaive(n, m):
		nTakeMFacLogE = _DecimalFns.ZERO
		for i in range(int(n),int(_DecimalContext.ctx.subtract(n, m)), -1):
			nTakeMFacLogE = _DecimalContext.ctx.add(nTakeMFacLogE, _DecimalContext.ctx.ln(Decimal(i)))
		return nTakeMFacLogE

	# in log space base 2
	@staticmethod
	def facultyNTakeMLog2(n, nLog2, m):
		nFacLog2 = _DecimalFns.facultyLog(n, nLog2, True)
		nSubM = _DecimalContext.ctx.subtract(n, m)
		nSubMLogE = _DecimalContext.ctx.ln(nSubM)
		nSubMFacLogE = _DecimalFns.facultyLog(nSubM, nSubMLogE, False) # in log space with base e
		nSubMFacLog2 = _DecimalContext.ctx.divide(nSubMFacLogE, _DecimalFns.LOG_E_2) # convert to log space with base 2 by dividing with ln(2), that is log_e_a = log_2_a / log_e_2
		nTakeMFacLog2 = _DecimalContext.ctx.subtract(nFacLog2, nSubMFacLog2)
		return nTakeMFacLog2

	# in e-log space
	@staticmethod
	def facultyNTakeMLogE(n, nLogE, m):
		nFacLogE = _DecimalFns.facultyLog(n, nLogE, False)
		nSubM = _DecimalContext.ctx.subtract(n, m)
		nSubMLogE = _DecimalContext.ctx.ln(nSubM)
		nSubMFacLogE = _DecimalFns.facultyLog(nSubM, nSubMLogE, False)
		nTakeMFacLogE = _DecimalContext.ctx.subtract(nFacLogE, nSubMFacLogE)
		return nTakeMFacLogE

	# faculty method wrapper for both natural and base-2 logarithms
	@staticmethod
	def facultyLog(n, nLog, isLog2):
		if _DecimalFns.isZero(n): # n == 0
			return _DecimalFns.ZERO
		else:
			if isLog2:
				return _DecimalFns.__facultyStirlingLog2(n, nLog)
			else:
				return _DecimalFns.__facultyStirlingLogE(n, nLog)

	'''
		Stirling's formula is an approximation for n!:

			n! 		~ 	(n/e)^n * sqrt(2 * pi * n)

		In log space with base e this is:

			ln(n!) 	~ 	ln((n/e)^n * sqrt(2 * pi * n))
					=	ln((n/e)^n) + ln(sqrt(2 * pi * n))
					=	n(ln(n/e)) + ln((2 * pi * n)^(1/2))
				 	=	n(ln(n) - ln(e)) + 0.5(ln(2) + ln(pi) + ln(n))
					= 	n(nLogE - 1) + 0.5(LOG_E_2 + LOG_E_PI + nLogE)
	'''
	# in e-log space
	@staticmethod
	def __facultyStirlingLogE(n, nLogE):
		t1InnerSubtrNFacLogE = _DecimalContext.ctx.subtract(nLogE, _DecimalFns.ONE)
		t1NFacLogE = _DecimalContext.ctx.multiply(n, t1InnerSubtrNFacLogE)
		t2NFacLogE = _DecimalContext.ctx.multiply(_DecimalFns.HALF, _DecimalContext.ctx.add(_DecimalContext.ctx.add(_DecimalFns.LOG_E_PI, _DecimalFns.LOG_E_2), nLogE))
		nFacLogE = _DecimalContext.ctx.add(t1NFacLogE, t2NFacLogE)
		return nFacLogE

	'''
		Stirling's formula in log base 2 space


			lg(n!) 	~ 	lg((n/e)^n * sqrt(2 * pi * n))
					=	lg((n/e)^n) + lg(sqrt(2 * pi * n))
					=	n(lg(n/e)) + lg((2 * pi * n)^(1/2))
				 	=	n(lg(n) - lg(e)) + 0.5(lg(2) + lg(pi) + lg(n))
					= 	n(nLog2 - LOG_2_E) + 0.5(1 + LOG_2_PI + nLog2
	'''
	# in 2-log
	@staticmethod
	def __facultyStirlingLog2(n, nLog2):
		t1InnerSubtrNFacLog2 = _DecimalContext.ctx.subtract(nLog2, _DecimalFns.LOG_2_E)
		t1NFacLog2 = _DecimalContext.ctx.multiply(n, t1InnerSubtrNFacLog2)
		t2NFacLog2 = _DecimalContext.ctx.multiply(_DecimalFns.HALF, _DecimalContext.ctx.add(_DecimalContext.ctx.add(_DecimalFns.LOG_2_PI, _DecimalFns.ONE), nLog2))
		nFacLog2 = _DecimalContext.ctx.add(t1NFacLog2, t2NFacLog2)
		return nFacLog2


class _BirthdayProblemSolver:

	########################################################################################################################################################################################################
	########################################################################################################################################################################################################
	#																																																	   #
	#	Wrapper class for solving the birthday problem by calling this program from another class in Python (_BirthdayProblemCLISolver assumes output to console or to JSON with formatting included       #
	#	where as this class only outputs the results)         																																			   #
	#																																																	   #
	########################################################################################################################################################################################################
	########################################################################################################################################################################################################

	# ways to calculate the birthday problem
	class CalcPrecision(Enum):
		EXACT = 1, # exact calculation (do not use for large numbers)
		STIRLING_APPROX = 2, # exact calculation but uses Stirling's formula for faculties which indirectly makes it an approximation
		TAYLOR_APPROX = 3, # uses an approximation of the main formula
		TRIVIAL = 4 # trivial solution where no calculation is needed

	'''
		Returns the probability p of at least one non-unique sample when sampling nOrNLog times from a set of size dOrDLog. If isBinary is true, dOrDLog, nOrNLog and the result are in base-2 logarithmic form.
		If isCombinations is true, then dOrDLog is the number of members, s, of a set from which we should generate the sample set d = s!. If both isBinary and isCombinations are true, then dOrDLog
		is the base-2 logarithm of the number of members, s, of a set from which we should generate the sample set d = (2^s)!. nOrNLog is not affected by the isCombinations flag.
	'''
	@staticmethod
	def solveForP(dOrDLog, nOrNLog, isBinary, isCombinations, method):
		_DecimalContext.reset() # reset to initial context precision
		_BirthdayProblemInputHandler.sanitize(dOrDLog, nOrNLog, None, isBinary, isCombinations, method == _BirthdayProblemSolver.CalcPrecision.STIRLING_APPROX, method == _BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX, method == _BirthdayProblemSolver.CalcPrecision.EXACT, False)
		d, dLog, n, nLog, _ = _BirthdayProblemInputHandler.setup(dOrDLog, nOrNLog, None, isBinary, isCombinations)
		if(dLog is None):
			raise SolverException(SolverErrorCode.DLOG_NOT_CALCULATED)
		return _BirthdayProblemSolverChecked.birthdayProblem(d, dLog, n, nLog, method, isBinary)

	'''
		Returns the number of samples n required to have a probability p of at least one non-unique sample when sampling from a set of size dOrDLog. If isBinary is true, dOrDLog and the result are in base-2 
		logarithmic form. If isCombinations is true, then dOrDLog is the number of members, s, of a set from which we should generate the sample set d (s!). If both isBinary and isCombinations are true, then 
		dOrDLog is the base-2 logarithm of the number of members, s, of a set from which we should generate the sample set d ((2^s)!).
	'''
	@staticmethod
	def solveForN(dOrDLog, p, isBinary, isCombinations):
		_DecimalContext.reset() # reset to initial context precision
		_BirthdayProblemInputHandler.sanitize(dOrDLog, None, p, isBinary, isCombinations, False, False, False, False)
		d, dLog, _, _, p = _BirthdayProblemInputHandler.setup(dOrDLog, None, p, isBinary, isCombinations)
		if(dLog is None):
			raise SolverException(SolverErrorCode.DLOG_NOT_CALCULATED)
		return _BirthdayProblemSolverChecked.birthdayProblemInv(d, dLog, p, isBinary)


class _BirthdayProblemSolverChecked:

	########################################################################################################################################################################################################
	########################################################################################################################################################################################################
	#																																																	   #
	#	Main drivers  that solves the birthday problem. Requires that input is checked and in correct form. Do not use directly, instead use BirthdayProblem.CLISolver or BirthdayProblem.Solver.          #
	#																																																	   #
	########################################################################################################################################################################################################
	########################################################################################################################################################################################################

	@staticmethod
	def birthdayProblem(maybeD, dLog, maybeN, nLog, calcPrecision, dIsLog2):
		# NOTE that dLog and nLog are 2 OR e base logarithms depending on input processing reflected in dIsLog2

		if (dIsLog2 and _DecimalFns.isLessThanOne(nLog)) or (not dIsLog2 and _DecimalFns.isLessThan(nLog, _DecimalFns.LOG_E_2)):
			# trivially, if you sample less than 2 times, the chance of a non-unique sample is 0%
			return (_DecimalFns.ZERO, _BirthdayProblemSolver.CalcPrecision.TRIVIAL)
		elif _DecimalFns.isGreaterThan(nLog, dLog):
			# trivially, if you sample more times than the number of items in the set to sample from, the chance of a non-unique item is 100%
			return (_DecimalFns.ONE, _BirthdayProblemSolver.CalcPrecision.TRIVIAL)
		else:

			if calcPrecision in [_BirthdayProblemSolver.CalcPrecision.EXACT, _BirthdayProblemSolver.CalcPrecision.STIRLING_APPROX] and (maybeD is None or maybeN is None):
				# d and n are needed for these methods
				raise SolverException(SolverErrorCode.D_NEEDED_FOR_METHOD, calcPrecision)

			# carry out the calculations
			_DecimalContext.adjustPrecision(maybeD.adjusted()) if maybeD is not None else _DecimalContext.adjustPrecision(dLog.adjusted())
			if calcPrecision == _BirthdayProblemSolver.CalcPrecision.EXACT:
				if _DecimalContext.isTooPrecise():
					# with a too high precision, even the simplest calculation takes too long
					raise SolverException(SolverErrorCode.TOO_HIGH_PRECISION, calcPrecision)
				if dIsLog2:
					return (_BirthdayProblemSolverChecked.__birthdayProblemExact(maybeD, _DecimalContext.ctx.divide(dLog, _DecimalFns.LOG_2_E), maybeN), _BirthdayProblemSolver.CalcPrecision.EXACT)
				else:
					return (_BirthdayProblemSolverChecked.__birthdayProblemExact(maybeD, dLog, maybeN), _BirthdayProblemSolver.CalcPrecision.EXACT)
			elif calcPrecision == _BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX:
				if _DecimalContext.isTooPrecise():
					_DecimalContext.adjustPrecision(dLog.adjusted())
					if _DecimalContext.isTooPrecise():
						# with a too high precision, even the simplest calculation takes too long
						raise SolverException(SolverErrorCode.TOO_HIGH_PRECISION, calcPrecision)
				if dIsLog2:
					return (_BirthdayProblemSolverChecked.__birthdayProblemTaylorApproxLog2(dLog, nLog), _BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX)
				else:
					return (_BirthdayProblemSolverChecked.__birthdayProblemTaylorApproxLogE(dLog, nLog), _BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX)
			else:
				if _DecimalContext.isTooPrecise():
					# with a too high precision, even the simplest calculation takes too long
					raise SolverException(SolverErrorCode.TOO_HIGH_PRECISION, calcPrecision)
				if dIsLog2:
					return (_BirthdayProblemSolverChecked.__birthdayProblemStirlingApproxLog2(maybeD, dLog, maybeN), _BirthdayProblemSolver.CalcPrecision.STIRLING_APPROX)
				else:
					return (_BirthdayProblemSolverChecked.__birthdayProblemStirlingApproxLogE(maybeD, dLog, maybeN), _BirthdayProblemSolver.CalcPrecision.STIRLING_APPROX)


	@staticmethod
	def birthdayProblemInv(maybeD, dLog, p, calcPrecision, dIsLog2):
		if _DecimalFns.isZero(p):
			# trivially, to have a 0% chance of picking a duplicate, just pick one sample (or 0)
			return (_DecimalFns.ZERO if dIsLog2 else _DecimalFns.ONE, _BirthdayProblemSolver.CalcPrecision.TRIVIAL)
		elif _DecimalFns.isOne(p) or _DecimalFns.isGreaterThanOne(p):
			# also trivially, to have a 100% (or more) chance of picking a duplicate, pick one more than the number of items in the input
			if dIsLog2:
				# if d is too large to calculate adding 1 to it is negligible
				return (dLog if maybeD is None else _DecimalContext.ctx.divide(_DecimalContext.ctx.ln(_DecimalContext.ctx.add(maybeD, _DecimalFns.ONE)), _DecimalFns.LOG_E_2), _BirthdayProblemSolver.CalcPrecision.TRIVIAL)
			else:
				# if d is too large to calculate adding 1 to it is negligible
				return (dLog if maybeD is None else _DecimalContext.ctx.add(maybeD, _DecimalFns.ONE), _BirthdayProblemSolver.CalcPrecision.TRIVIAL)
		elif _DecimalFns.isZero(dLog):
			# set size is 1 and p is neither 0 nor 1, for ANY p in between 0 and 1, 2 samples are required to get a non-unique sample
			return (_DecimalFns.ONE if dIsLog2 else _DecimalFns.TWO, _BirthdayProblemSolver.CalcPrecision.TRIVIAL)
		else:
			if calcPrecision in [_BirthdayProblemSolver.CalcPrecision.EXACT] and (maybeD is None):
				# d is needed for this method
				raise SolverException(SolverErrorCode.D_NEEDED_FOR_METHOD, calcPrecision)

			# carry out the calculations
			_DecimalContext.adjustPrecision(maybeD.adjusted()) if maybeD is not None else _DecimalContext.adjustPrecision(dLog.adjusted())
			if calcPrecision == _BirthdayProblemSolver.CalcPrecision.EXACT:
				if _DecimalContext.isTooPrecise():
					# with a too high precision, even the simplest calculation takes too long
					raise SolverException(SolverErrorCode.TOO_HIGH_PRECISION, calcPrecision)
				if dIsLog2:
					return (_DecimalContext.ctx.divide(
						_DecimalContext.ctx.ln(
							_BirthdayProblemSolverChecked.__birthdayProblemInvExact(maybeD, p)
						),
						_DecimalFns.LOG_E_2
					), _BirthdayProblemSolver.CalcPrecision.EXACT)
				else:
					return (_BirthdayProblemSolverChecked.__birthdayProblemInvExact(maybeD, p), _BirthdayProblemSolver.CalcPrecision.EXACT)
			else:
				if _DecimalContext.isTooPrecise():
					_DecimalContext.adjustPrecision(dLog.adjusted())
					if _DecimalContext.isTooPrecise():
						# with a too high precision, even the simplest calculation takes too long
						raise SolverException(SolverErrorCode.TOO_HIGH_PRECISION, _BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX)
				if dIsLog2:
					return (_BirthdayProblemSolverChecked.__birthdayProblemInvTaylorApproxLog2(dLog, p), _BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX)
				else:
					return (_DecimalContext.ctx.exp(_BirthdayProblemSolverChecked.__birthdayProblemInvTaylorApproxLogE(dLog, p)), _BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX)

	########################################################################################################################################################################################################
	########################################################################################################################################################################################################
	#																																																	   #
	#	Internal drivers                 																																								   #
	#																																																	   #
	########################################################################################################################################################################################################
	########################################################################################################################################################################################################

	'''
		A frequent formula in the context of the birthday problem (or paradox) calculates the chance of no two items being equal (all items unique) when drawing d (picked) items from a population of n 
		(possibilities) items. Since we can choose unique items from n in (n)_d ways, and you can pick d items (any) from n in n^d, the formula for this is:

			^P(n, d) 	= (n)_d / n^d

		In log space, this is:

			lg(^P(n, d))= lg((n)_d / n^d)
						= lg((n)_d) - lg(n^d)
						= lg((n)_d) - d * lg(n) 

		This result calculates the chance of all items unique, but most often, we are interested in the chance of there being at least one (trivially two) non-unique item(s) among dm P(n, d), which is 
		why we take the complement of ^P(n, d) as the final result of these functions.

			P(n, d) 	= 1 - ^P(n, d)
	'''

	@staticmethod
	def __birthdayProblemExact(d, dLogE, n):
		favourableLogE = _DecimalFns.facultyNTakeMNaive(d, n)
		possibleLogE = _DecimalContext.ctx.multiply(dLogE, n)
		negProbLogE = _DecimalContext.ctx.subtract(favourableLogE, possibleLogE)
		negProb = _DecimalContext.ctx.exp(negProbLogE)
		prob = _DecimalContext.ctx.subtract(_DecimalFns.ONE, negProb) # complement
		return prob

	# calculates result in base 2 logarithmic space with base 2. Outputs probability in [0, 1]. Assumes non-trivial solution.
	@staticmethod
	def __birthdayProblemStirlingApproxLog2(d, dLog2, n):
		favourableLog2 = _DecimalFns.facultyNTakeMLog2(d, dLog2, n) # numerator
		possibleLog2 = _DecimalContext.ctx.multiply(dLog2, n) # denominator
		negProbLog2 = _DecimalContext.ctx.subtract(favourableLog2, possibleLog2) # division in log space is subtraction
		negProb = _DecimalContext.ctx.power(_DecimalFns.TWO, negProbLog2) # go back to non-logarithmic space
		prob = _DecimalContext.ctx.subtract(_DecimalFns.ONE, negProb) # complement
		return prob if(_DecimalFns.isGreaterThanZero(prob)) else _DecimalFns.ZERO # fix precision errors leading to negative result

	# calculates the result in natural base logarithms.
	@staticmethod
	def __birthdayProblemStirlingApproxLogE(d, dLogE, n):
		favourableLogE = _DecimalFns.facultyNTakeMLogE(d, dLogE, n) # numerator
		possibleLogE = _DecimalContext.ctx.multiply(dLogE, n)
		negProbLogE = _DecimalContext.ctx.subtract(favourableLogE, possibleLogE) # division in log space is subtraction
		negProb = _DecimalContext.ctx.exp(negProbLogE) # back to non-logarithmic space
		prob = _DecimalContext.ctx.subtract(_DecimalFns.ONE, negProb)
		return prob if(_DecimalFns.isGreaterThanZero(prob)) else _DecimalFns.ZERO # fix precision errors leading to negative result


	'''
		In the previous versions we used an exact version of the main formula, even though Stirling's approximation was used for faculties. In the next version, we use an approximation for the main formula
		which is based on Taylor series. This approximation is the best one available (it might be improved by adding other terms but the method is still the same).

		The formula is based on the observation that ln(n!) = ln(n) + ln(n - 1) + ... + ln(1): 

			P(n, d) 			~ 1 - e^(-(n^2/2d))
			
		NOTE: this is really an approximation of the approximation; substitute n^2 for n * (n - 1) is possible
		for a more accurate formula.

		This implies that

			^P(n, d)			~ e^(-(n^2/2d))

		In natural log space this is:

			ln(^P(n, d))		~ ln(e^(-(n^2/2d)))
								= -(n^2/2d)

		This implies
			
			-ln(^P(n, d))		~ (n^2/2d)

		Now, for any logarithmic base (including natural), we now get by taking logarithms again

			lg(-ln(^P(n, d)))	~ lg(n^2/2d)

		lg(-ln(^P(n, d))) is actually defined in the real domain here since 0.0 <= ^P(n, d) <= 1.0, which gives that ln(^P(n ,d)) <= 0), which gives -ln(^P(n, d)) >= 0
								
								= lg(n^2) - lg(2d)
								= 2 * lg(n) - (lg(2) + lg(d))

		For base-2 logarithms, this yields:

			lg(-ln(^P(n, d)))	~ 2 * lg(n) - (lg(2) + lg(d))
								= 2 * nLog2 - (1 + dLog2)
								
		Connecting back to the previous NOTE, 2 * lg(n) comes from lg(n^2), with the more accurate formula we would
		instead have lg(n * (n - 1)) which equals lg(n) + lg(n - 1). This requires us to have n available. Note that
		on a simplistic note, one might be aware of this improvement but still omit it since we then stay more true to
		the approximation in use here. Therefore it has been omitted below.
	'''

	# calculates result in base-2 logarithms (second level of logs)
	@staticmethod
	def __birthdayProblemTaylorApproxLog2(dLog2, nLog2):
		t1NegProbMinusLogELog2 = _DecimalContext.ctx.multiply(nLog2, _DecimalFns.TWO)
		t2NegProbMinusLogELog2  = _DecimalContext.ctx.add(Decimal(dLog2), _DecimalFns.ONE)
		negProbMinusLogELog2 = _DecimalContext.ctx.subtract(t1NegProbMinusLogELog2 , t2NegProbMinusLogELog2 )
		negProbMinusLogE = _DecimalContext.ctx.power(_DecimalFns.TWO, negProbMinusLogELog2) # go back to non-logarithmic space
		negProbLogE = _DecimalContext.ctx.minus(negProbMinusLogE)
		negProb = _DecimalContext.ctx.exp(negProbLogE)
		prob = _DecimalContext.ctx.subtract(_DecimalFns.ONE, negProb) # complement
		return prob

	'''
		For base-e logarithms, the last part of the previous section yields:

			ln(-ln(^P(n, d)))	~ 2 * ln(n) - (ln(2) + ln(d))
								= 2 * nLogE - (LOG_E_2 + dLogE)
								
		Again connecting back to the previous NOTE, 2 * ln(n) comes from ln(n^2), with the more accurate formula we 
		would instead have ln(n * (n - 1)) which equals ln(n) + ln(n - 1). This requires us to have n available. Note 
		that on a simplistic note, one might be aware of this improvement but still omit it since we then stay more 
		true to the approximation in use here. Therefore it has been omitted below.
	'''
	# calculates result in natural logarithmic space
	@staticmethod
	def __birthdayProblemTaylorApproxLogE(dLogE, nLogE):
		t1NegProbMinusLogELogE = _DecimalContext.ctx.multiply(nLogE, _DecimalFns.TWO)
		t2NegProbMinusLogELogE  = _DecimalContext.ctx.add(Decimal(dLogE), _DecimalFns.LOG_E_2)
		negProbMinusLogELogE = _DecimalContext.ctx.subtract(t1NegProbMinusLogELogE , t2NegProbMinusLogELogE)
		negProbMinusLogE = _DecimalContext.ctx.exp(negProbMinusLogELogE) # go back to non-logarithmic space
		negProbLogE = _DecimalContext.ctx.minus(negProbMinusLogE)
		negProb = _DecimalContext.ctx.exp(negProbLogE)
		prob = _DecimalContext.ctx.subtract(_DecimalFns.ONE, negProb) # complement
		return prob

	'''
		The formula for the forward birthday problem is
		
		    P(n, d) 			= 1 - (1 - 1/d) * (1 - 2/d) * ... * (1 - (n - 1)/d)
		    P(n, d) 			= 1 - ((d - 1)/d) * ((d - 2)/d) * ... * ((d - (n - 1))/d)
		
		Remember, this P(n, d) is the probability of a collision.
		
		which leads to
			^P(n, d)			= ((d - 1)/d) * ((d - 2)/d) * ... * ((d - (n - 1))/d)
			
		which is the probability of all unique, which in log space is
		
			ln(^P(n, d))		= ln(((d - 1)/d) * ((d - 2)/d) * ... * ((d - (n - 1))/d))
								= ln((d - 1)/d) + ln((d - 2)/d) + ... + ln((d - (n - 1))/d)
								= ln(d - 1) - ln(d) + ln(d - 2) - ln(d) + ... + ln(d - (n - 1)) - ln(d)
			
		We want to find n such that P(n, d) >= Pin (input p), e.g. the number of samples needed for the probability of a
		collision to be equal to or higher than Pin. This means that we need to find n such that P^(n, d) < 1 - Pin.
		The first such value for n entails a P(n, d) >= Pin. In log space y = ln(x), probabilities from 0 to 1 map to 
		y value from negative infinity to 0. We start with a single sample for which the probability of all samples
		unique is 1. For every added sample, this probability decreases towards 1 - Pin until it is less than 1 - Pin
		at which point we have found the relevant n.
						
		If we want to use a naive and exact method, we can calculate n numerically by adding one term to the sum until
		ln(^P(n, d)) <= ln(1 - P)
		
		Note that for some reason, these calculations are faster in non-logarithmic space, perhaps due to the ln 
		operation taking more time than is won off of using add / subtract in logarithmic space rather than multiply
		/ divide in regular space.
		
		Also note that the first term in the above calculation is really 1 with a probability of all unique being 1.
		Already when we calculate 1 * (d - 1 /d) we are assuming 2 samples. Thus the value of n is really reflecting
		how many ADDITIONAL people to the initial one that is needed for the calculated probability. We thus make
		up for this by adding 1 to the final result.
	'''
	@staticmethod
	def __birthdayProblemInvExact(d, p):
		pInv = _DecimalContext.ctx.subtract(_DecimalFns.ONE, p)
		n = _DecimalFns.ONE
		currentPInv = _DecimalContext.ctx.divide(_DecimalContext.ctx.subtract(d, n), d)
		while currentPInv > pInv:
			n = _DecimalContext.ctx.add(n, _DecimalFns.ONE)
			currentPInv = _DecimalContext.ctx.multiply(
				currentPInv,
				_DecimalContext.ctx.divide(_DecimalContext.ctx.subtract(d, n), d)
			)
		final = _DecimalContext.ctx.add(n, _DecimalFns.ONE)
		return final

	'''
		The formula for calculating the inverted birthday problem, namely how many times to sample from a set to reach a probability p of some non-unique samples, also uses the above Taylor approximation.

		Starting, from the previous section, with:

			P(n, d) 			~ 1 - e^(-(n^2/2d))

		We have:

			^P(n, d) 			~ e^(-(n^2/2d))

		Trying to solve for n, we get:

			ln(^P(n, d))		~ (-(n^2/2d))
			-ln(^P(n, d))		~ (n^2/2d)
			-ln(^P(n, d))) * 2d ~ n^2
			n 					~ sqrt(-ln(^P(n, d))) * 2d)
			n(P, d)				~ sqrt(-ln(^P) * 2d)
		
		The above works for the same reason as stated earlier. -ln(^P) >= 0 since ^P <= 1.0 and so the value in sqrt() is positive.
		Using logarithms to solve this, we have:

			lg(n(P, d))			~ lg(sqrt(-ln(^P) * 2d))
								= lg((-ln(^P) * 2d)^(1/2))
								=	0.5 * lg(-ln(^P) * 2d)
								= 0.5 * ( lg(-ln(^P)) + lg(2d) )
								= 0.5 * ( lg(-ln(^P)) + (lg(2) + lg(d)))
								= 0.5 * ( lg(-ln(^P)) + lg(2) + lg(d) )

		Working with P, instead of ^P, we have:

			lg(n(P, d))			~ 0.5 * ( lg(-ln(1 - P)) + lg(2) + lg(d) )

		For natural logarithms we arrive at:

			lg(n(P, d))			~ 0.5 * ( ln(-ln(1 - P)) + ln(2) + ln(d))
								= 0.5 * ( ln(-ln(1 - p)) + LOG_E_2 + dLogE )
								
		NOTE that this calculation uses the approximation of the approximation using n^2 instead of the more accurate
		n * (n - 1). Of course this is necessary here since we need to be able to do the root calculation to arrive at
		an answer. The forward formula however may take (it currently doesn't) the less coarse approximation into 
		account whereby the forward and backward calculations may differ when verifying n(P, d) in P(n, d) with the 
		Taylor approximation.
	'''
	# with base e logarithms
	@staticmethod
	def __birthdayProblemInvTaylorApproxLogE(dLogE, p):
		t1SamplesLogE2 = _DecimalContext.ctx.ln(_DecimalContext.ctx.subtract(_DecimalFns.ONE, p))
		t1SamplesLogE = _DecimalContext.ctx.ln(_DecimalContext.ctx.minus(t1SamplesLogE2))
		samplesLogE = _DecimalContext.ctx.multiply(_DecimalFns.HALF, _DecimalContext.ctx.add(t1SamplesLogE, _DecimalContext.ctx.add(_DecimalFns.LOG_E_2, dLogE)))
		return samplesLogE

	'''
		For base 2 logarithms we arrive at:

			lg(n(P, d))			~ 0.5 * ( lg(-ln(1 - P)) + lg(2) + lg(d) )
								= 0.5 * ( lg(-ln(1 - P)) + 1 + dLog2 )
	'''
	# with base 2 logarithms
	@staticmethod
	def __birthdayProblemInvTaylorApproxLog2(dLog2, p):
		dLogE = _DecimalContext.ctx.divide(dLog2, _DecimalFns.LOG_2_E) # go to natural logarithms
		samplesLogE = _BirthdayProblemSolverChecked.__birthdayProblemInvTaylorApproxLogE(dLogE, p)
		samplesLog2 = _DecimalContext.ctx.divide(samplesLogE, _DecimalFns.LOG_E_2) # back to base 2 logarithms
		return samplesLog2

class _BirthdayProblemNumberFormatter:

	########################################################################################################################################################################################################
	########################################################################################################################################################################################################
	#																																																	   #
	#	Output formatting functions to format the resulting numbers only. Used by BirthdayProblem.CLISolver to output numbers in a nice form.										  			 		   #
	#																																																	   #
	########################################################################################################################################################################################################
	########################################################################################################################################################################################################

	# threshold outside which we also print values in log10 space
	LOG10_LOWER_THRESHOLD = Decimal('1e-2')
	LOG10_UPPER_THRESHOLD = Decimal('1e+5')

	# default decimal precision of output
	OUTPUT_PRECISION = 10

	# error constant for floating point rounding
	ERR = Decimal('1e-12')

	# compare number dBase^dExp10 to originalD and see whether they differ, relatively, by more than ERR or not. This implies filtering out a common power of 10 and then comparing the results. The reason is
	# to determine whether to use approximation or equality sign.
	@staticmethod
	def isExpReprEqualToStandardRepr(dBase, dExp10, originalD):
		originalDExp = originalD.adjusted() # powers of 10 to filter out from the original input
		originalD = _DecimalContext.ctx.divide(originalD, _DecimalContext.ctx.power(_DecimalFns.TEN, Decimal(originalDExp)))
		base10PowersDiff =  dExp10 - originalDExp # scale dBase so that they have the same number of powers of 10 filtered out
		leveledD = _DecimalContext.ctx.multiply(dBase, _DecimalContext.ctx.power(_DecimalFns.TEN, Decimal(base10PowersDiff)))
		equal = _DecimalFns.isLessThan(_DecimalContext.ctx.abs(_DecimalContext.ctx.subtract(originalD, leveledD)), _BirthdayProblemNumberFormatter.ERR)
		return equal

	# returns log10 representation of a number or the empty string if the input is not outside the defined log10 representation thresholds.
	@staticmethod
	def toLog10ReprOrNone(argD):
		if(_DecimalFns.isGreaterThan(_BirthdayProblemNumberFormatter.LOG10_LOWER_THRESHOLD, argD) or _DecimalFns.isLessThan(_BirthdayProblemNumberFormatter.LOG10_UPPER_THRESHOLD, argD)) and _DecimalFns.isGreaterThanZero(argD):
			# d is smaller than the lower log 10 repr threshold or larger than the upper log 10 repr threshold, and not 0, so a complementary log 10 representation is called for
			(sign, digits, exp) = Context(prec=1, rounding=ROUND_HALF_UP).create_decimal(argD).as_tuple()
			d = Decimal(str(digits[0]))
			equalOrApprox = "=" if _BirthdayProblemNumberFormatter.isExpReprEqualToStandardRepr(d, exp, argD) else "≈"
			return equalOrApprox + (str(d) + "*" if _DecimalFns.isNotOne(d) else "")  + "10^" + str(exp)
		else:
			return  "" # no base 10 representation needed

	@staticmethod
	def toOutputNumberFormatted(d, prec = None):
		if prec is None:
			prec = _BirthdayProblemNumberFormatter.OUTPUT_PRECISION
		return _BirthdayProblemNumberFormatter.toOutputNumber(('{:.' + str(prec) + 'f}').format(d))

	@staticmethod
	def toFloatRoundedAndApproximate(f, prec = None, returnParts = False):
		roundedF = _BirthdayProblemNumberFormatter.toOutputNumberFormatted(f, prec)
		prefix = "≈" if _DecimalFns.areNotEqual(f, Decimal(roundedF)) else ""
		return (prefix, roundedF) if returnParts else prefix + roundedF

	@staticmethod
	def toIntegralRounded(d, rounding = ROUND_HALF_UP):
		roundedD = d.to_integral_value(rounding)
		return ("", str(roundedD))

	@staticmethod
	def toIntegralRoundedAndApproximate(d, returnParts = False):
		roundedD = d.to_integral_value()
		prefix = "≈" if _DecimalFns.areNotEqual(d, roundedD) else ""
		return (prefix, str(roundedD)) if returnParts else prefix + str(roundedD)

	@staticmethod
	def toOutputNumber(out):
		if out.find(".") != -1:
			out = out.rstrip("0")
			out = out.rstrip(".")
		return out

class _BirthdayProblemTextFormatter:

	########################################################################################################################################################################################################
	########################################################################################################################################################################################################
	#																																																	   #
	#	Text output formatting functions to format the text only. Used by BirthdayProblem.CLISolver.solve() to output text in a nice way.													               #
	#																																																	   #
	########################################################################################################################################################################################################
	########################################################################################################################################################################################################

	INDENT_SZ = 10

	@staticmethod
	def parenthesize(text):
		if text != "":
			return " (" + text + ")"
		else:
			return text

	@staticmethod
	def methodToShortDescription(method):
		texts = {
			_BirthdayProblemSolver.CalcPrecision.EXACT: "Exact method",
			_BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX: "Taylor approximation",
			_BirthdayProblemSolver.CalcPrecision.STIRLING_APPROX: "Exact method with Stirling's approximation",
			_BirthdayProblemSolver.CalcPrecision.TRIVIAL: "Trivial method"
		}
		return texts.get(method, "Unknown method")

	@staticmethod
	def methodToText(method):
		texts = {
			_BirthdayProblemSolver.CalcPrecision.EXACT: "Exact",
			_BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX: "Taylor",
			_BirthdayProblemSolver.CalcPrecision.STIRLING_APPROX: "Stirling",
			_BirthdayProblemSolver.CalcPrecision.TRIVIAL: "Trivial"
		}
		return texts.get(method, "Unknown")

	@staticmethod
	def methodToDescription(method, isInv):
		texts = {
			_BirthdayProblemSolver.CalcPrecision.EXACT: "Exact method",
			_BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX: "Taylor series approximation used in main calculation" + ("" if isInv else " (removes need for factorial calculation)"),
			_BirthdayProblemSolver.CalcPrecision.STIRLING_APPROX: "Stirling's approximation used in factorial calculation",
			_BirthdayProblemSolver.CalcPrecision.TRIVIAL: "Trivial solution"
		}
		return texts.get(method, "Unknown method")

	@staticmethod
	def headerTextBirthdayProblemInvNumbers(dLogOrNot, p, pPercent, isLog2, prec = None):
		if isLog2:
			dLog2Text = "2^"
			dLog10Text = ""
			(prefix, dText) = _BirthdayProblemNumberFormatter.toFloatRoundedAndApproximate(dLogOrNot, prec, True)
		else:
			dLog2Text = ""
			dLog10Text = _BirthdayProblemTextFormatter.parenthesize(_BirthdayProblemNumberFormatter.toLog10ReprOrNone(dLogOrNot))
			(prefix, dText) = _BirthdayProblemNumberFormatter.toIntegralRoundedAndApproximate(dLogOrNot, True)
		pLog10Text = _BirthdayProblemTextFormatter.parenthesize(_BirthdayProblemNumberFormatter.toLog10ReprOrNone(p))
		return prefix + dLog2Text + dText + dLog10Text, _BirthdayProblemNumberFormatter.toFloatRoundedAndApproximate(pPercent, prec) + "%" + pLog10Text

	@staticmethod
	def headerTextBirthdayProblemInv(dLogOrNot, p, pPercent, isLog2, prec = None):
		dText, pText = _BirthdayProblemTextFormatter.headerTextBirthdayProblemInvNumbers(dLogOrNot, p, pPercent, isLog2, prec)
		return "The number of samples, sampled uniformly at random from a set of " + dText + " items, needed to have at least a " + pText + " chance of a non-unique sample is:"

	@staticmethod
	def resultTextBirthdayProblemInvNumbers(n, isLog2, prec = None):
		if isLog2:
			nLog2Text = "2^"
			nLog10Text = ""
			(prefix, nText) = _BirthdayProblemNumberFormatter.toFloatRoundedAndApproximate(n, prec, True)
		else:
			nLog2Text = ""
			nLog10Text = _BirthdayProblemTextFormatter.parenthesize(_BirthdayProblemNumberFormatter.toLog10ReprOrNone(n))
			(prefix, nText) = _BirthdayProblemNumberFormatter.toIntegralRounded(n, ROUND_CEILING)
		return prefix + nLog2Text + nText, nLog10Text

	@staticmethod
	def resultTextBirthdayProblemInv(n, isLog2, method, prec = None):
		nText, nLog10Text = _BirthdayProblemTextFormatter.resultTextBirthdayProblemInvNumbers(n, isLog2, prec)
		return (nText, nLog10Text, _BirthdayProblemTextFormatter.parenthesize(_BirthdayProblemTextFormatter.methodToDescription(method, True)))

	@staticmethod
	def headerTextBirthdayProblemNumbers(dLogOrNot, nLogOrNot, isLog2, prec = None):
		if isLog2:
			log2Text = "2^"
			dLog10Text = nLog10Text = ""
			(prefix, dText) = _BirthdayProblemNumberFormatter.toFloatRoundedAndApproximate(dLogOrNot, prec, True)
		else:
			log2Text = ""
			dLog10Text = _BirthdayProblemTextFormatter.parenthesize(_BirthdayProblemNumberFormatter.toLog10ReprOrNone(dLogOrNot))
			nLog10Text = _BirthdayProblemTextFormatter.parenthesize(_BirthdayProblemNumberFormatter.toLog10ReprOrNone(nLogOrNot))
			(prefix, dText) = _BirthdayProblemNumberFormatter.toIntegralRoundedAndApproximate(dLogOrNot, True)
		return prefix + log2Text + dText + dLog10Text, log2Text + str(nLogOrNot) + nLog10Text

	@staticmethod
	def headerTextBirthdayProblem(dLogOrNot, nLogOrNot, isLog2, prec = None):
		dText, nText = _BirthdayProblemTextFormatter.headerTextBirthdayProblemNumbers(dLogOrNot, nLogOrNot, isLog2, prec)
		return "The probability of finding at least one non-unique sample among " + nText + " samples, sampled uniformly at random from a set of " + dText + " items, is:"

	@staticmethod
	def resultTextBirthdayProblemNumbers(p, pPercent, prec = None):
		pLog10Text = _BirthdayProblemTextFormatter.parenthesize(_BirthdayProblemNumberFormatter.toLog10ReprOrNone(p))
		return _BirthdayProblemNumberFormatter.toFloatRoundedAndApproximate(pPercent, prec) + "%", pLog10Text

	@staticmethod
	def resultTextBirthdayProblem(p, pPercent, method, prec = None):
		pText, pLog10Text = _BirthdayProblemTextFormatter.resultTextBirthdayProblemNumbers(p, pPercent, prec)
		return (pText, pLog10Text, _BirthdayProblemTextFormatter.parenthesize(_BirthdayProblemTextFormatter.methodToDescription(method, False)))

	@staticmethod
	def indented(text):
		return (" " * _BirthdayProblemTextFormatter.INDENT_SZ) + text

class _BirthdayProblemInputHandler:

	########################################################################################################################################################################################################
	########################################################################################################################################################################################################
	#																																																	   #
	#	Input sanitizer		            																																								   #
	#																																																	   #
	########################################################################################################################################################################################################
	########################################################################################################################################################################################################

	@staticmethod
	def illegalInputString(varName = None):
		return "Illegal input" if varName is None else "Illegal input for '" + varName + "'"

	@staticmethod
	def checkType(var, type, varName, typeName):
		if(not isinstance(var, type)):
			raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString(varName) + ": must be of type '" + typeName + "'")

	@staticmethod
	def checkDecimal(var, varName):
		return _BirthdayProblemInputHandler.checkType(var, Decimal, varName, "Decimal")

	@staticmethod
	def checkBoolean(var, varName):
		return _BirthdayProblemInputHandler.checkType(var, bool, varName, "bool")

	# method that takes the input and checks the arguments and their semantic joint meaning and throws an error if it is not accepted
	@staticmethod
	def sanitize(dOrDLog, nOrNLog, p, isBinary, isCombinations, isStirling, isTaylor, isExact, isAll, varMap = {}):
		if dOrDLog is None:
			raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString(varMap.get("dOrDLog", "dOrDLog")) + ": please provide a size for the set to sample from.")
		_BirthdayProblemInputHandler.checkDecimal(dOrDLog, varMap.get("dOrDLog", "dOrDLog"))

		for [var, varName] in [[isBinary, varMap.get("isBinary", "isBinary")], [isCombinations, varMap.get("isCombinations", "isCombinations")], [isStirling, varMap.get("isStirling", "isStirling")], [isTaylor, varMap.get("isTaylor", "isTaylor")], [isExact, varMap.get("isExact", "isExact")], [isAll, varMap.get("isAll", "isAll")]]:
			_BirthdayProblemInputHandler.checkBoolean(var, varName)

		if not _DecimalFns.isInteger(dOrDLog):
			raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString(varMap.get("dOrDLog", "dOrDLog")) + ": please provide an integer")
		elif _DecimalFns.isLessThanZero(dOrDLog):
			raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString(varMap.get("dOrDLog", "dOrDLog")) + ": please provide a non-negative integer")
		elif(_DecimalFns.isZero(dOrDLog) and not isBinary and not isCombinations):
			raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString(varMap.get("dOrDLog", "dOrDLog")) + ": please provide a value for '" + varMap.get("dOrDLog", "dOrDLog") + "' that results in a non-empty set of unique items from which samples are taken.")

		if (p is None and nOrNLog is None) or (p is not None and nOrNLog is not None):
			raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString() + ": please provide a non-None value for either '" + varMap.get("nOrDLog", "nOrDLog") + "' or '" + varMap.get("p", "p") + "' (not both)")

		if nOrNLog is not None:
			_BirthdayProblemInputHandler.checkDecimal(nOrNLog, varMap.get("nOrDLog", "nOrDLog"))
			if not isStirling and not isExact and not isTaylor and not isAll:
				raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString() + ": must set at least one of '" + varMap.get("isStirling", "isStirling") + "', '" + varMap.get("isTaylor", "isTaylor") + "', '" + varMap.get("isExact", "isExact") + "' or '" + varMap.get("isAll", "isAll") + "'.")
			elif (isStirling or isExact or isTaylor) and isAll:
				raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString() + ": flag '" + varMap.get("isAll", "isAll") + "' was true and implicitly includes '" + varMap.get("isStirling", "isStirling") + "' (with -n), '" + varMap.get("isTaylor", "isTaylor") + "' and '" + varMap.get("isExact", "isExact") + "' set to True which should then not be set to True.")
			elif not _DecimalFns.isInteger(nOrNLog):
				raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString(varMap.get("nOrDLog", "nOrDLog")) + ": please provide an integer")
			elif _DecimalFns.isLessThanZero(nOrNLog):
				raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString(varMap.get("nOrDLog", "nOrDLog")) + ": please provide a non-negative integer")

		else:
			_BirthdayProblemInputHandler.checkDecimal(p, varMap.get("p", "p"))
			if isStirling:
				raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString() + ": '" + varMap.get("isStirling", "isStirling") + "' should only be non-False when '" + varMap.get("nOrDLog", "nOrDLog") + "' is not None.")
			elif _DecimalFns.isGreaterThanOne(p) or _DecimalFns.isLessThanZero(p):
				raise SolverException(SolverErrorCode.BAD_INPUT, message = _BirthdayProblemInputHandler.illegalInputString(varMap.get("p", "p")) + ": please provide a non-negative decimal number in the range [0.0, 1.0]")

	# further processes correct input and extract all arguments that is needed for calculations to start (based on isBinary and isCombinations)
	@staticmethod
	def setup(dOrDLog, nOrNLog, p, isBinary, isCombinations):
		d = dOrDLog
		dLog = None
		n = nOrNLog
		nLog = None

		# prepare by taking isBinary and sCombinations flags into account to established the actual sizes of d and dLogD
		try:
			if isCombinations:
				# d is the size of a set of items, calculate the number of permutations that is possible with it
				if isBinary:
					dLog = _DecimalFns.facultyLog(_DecimalContext.ctx.power(_DecimalFns.TWO, dOrDLog), dOrDLog, True)
					d = _DecimalContext.ctx.power(_DecimalFns.TWO, dLog)
				else:
					dLog = _DecimalFns.facultyLog(d, _DecimalContext.ctx.ln(dOrDLog), False)
					d = _DecimalContext.ctx.exp(dLog)
			else:
				# d is already the size of the set of combinations
				if isBinary:
					dLog = dOrDLog
					d = _DecimalContext.ctx.power(_DecimalFns.TWO, dOrDLog)
				else:
					dLog = _DecimalContext.ctx.ln(dOrDLog)
		except Overflow:
			d = None # either calculation of dLog threw and then dLog remains None and d is larger and definitely not calculated = None, or just calc of d threw which means d should be None

		if p is None:
			# calculate probability p based on d and n
			try:
				if isBinary:
					nLog = nOrNLog
					n = _DecimalContext.ctx.power(_DecimalFns.TWO, nLog)
				else:
					# for all purposes, sampling 0 times is the same as samping 1 times
					nLog = _DecimalContext.ctx.ln(nOrNLog) if(_DecimalFns.isGreaterThanZero(nOrNLog)) else _DecimalFns.ZERO
			except Overflow:
				n = None # calc of n threw which means n should be None

		return (d, dLog, n, nLog, p)

class _BirthdayProblemInputParser:

	########################################################################################################################################################################################################
	########################################################################################################################################################################################################
	#																																																	   #
	#	Input parser used by Birthday.CLISolver to parse input arguments 																								      							   #
	#																																																	   #
	########################################################################################################################################################################################################
	########################################################################################################################################################################################################

	@staticmethod
	def parse(args = None):
		parser = argparse.ArgumentParser(
			description="Treats the generalized birthday problem for arbitrary values.\n\nCalculates the generalized birthday problem, the probability P that, when sampling uniformly at random N times (with replacement)"
			+ " from a set of D unique items, there is a non-unique item among the N samples. In the original birthday problem formulation, N is 23 and D is 366 (or 365) for a risk of P ≈ 0.5 = 50% of at least two people having the same"
			+ " birthday.\n\nSupports calculating both the probability P from N and D (using exact method, exact method with Stirling's approximation in the calculation of faculties and Taylor approximation) and N"
			+ " from D and P (using exact method and Taylor approximation). Both approximations get asymptotically close to the exact result as D grows towards infinity. The exact method should not be used for larger numbers. For extremely"
			+ " small probabilities P, the exact method with Stirling's approximation used for faculties may become unstable as it involves many more different operations than the Taylor approximation which, each, results in small round-offs."
			+ " Another source of error in this case arises from the use of Stirling's formula for two calculations of faculties (D! and (D - N)!). Since one of these ((D - N)!) diverges slightly more from the exact result than the other (D!),"
			+ " the difference between these (used for calculations in log space) might introduce small errors when P is extremely small. A good check to see whether the approximation in question is suffering or not is to compare it to the Taylor"
			+ " approximation and see whether they match well.\n\nInputs D and N can be seen as literal input numbers or as exponents of base 2 (with -b flag). Furthermore, input D can be seen as a set of items from which"
			+ " we should produce the D! permutations before proceeding with further calculations (with flag -c).\n\nExample usage:\n\n    Example 1:\n        Calculate the probability P of at least one non-unique birthday among N = 23 persons with all available methods:\n"
			+ "        > python BirthdayProblem.py 366 -n 23 -a\n\n    Example 2:\n        Calculate, with Taylor approximation, the number of times N a deck of cards has to be shuffled to have a P = 50% probability of seeing a repeated shuffle:\n        > python BirthdayProblem.py 52 -p 0.5 -t -c\n\n    Example 3:\n"
			+ "        Calculate, with approximative methods, the probability P of a collision in a 128-bit crypto when encrypting N = 2^64 = 18 446 744 073 709 551 616 blocks with the same key and output answer as a Json object with at most 5 decimals:\n        > python BirthdayProblem.py 128 -n 64 -b -s -t -j --prec 5",
			formatter_class=argparse.RawTextHelpFormatter
		)

		parser.add_argument('d', metavar=('D'), type=str, nargs=1, help='Input number D, the total number of unique items, or a number from which the total number of unique items can be derived, in the set we are sampling from.')
		parser.add_argument('-n', '--samples', metavar=('N'), type=str, help='Input number N, the number of samples, or a number from which the number of samples can be derived from, taken from the full set of D items. When present the probability P of at least one non-unique item among the samples will be calculated. Requires one of flags -e, -s, -t or -a to determine the desired precision(s) of the calculation.')
		parser.add_argument('-p', '--probability', metavar=('P'), type=str, help='Input number P in [0.0, 1.0], the the probability of at least one non-unique item among the samples. When present the needed number of samples N will be calculated. Requires one of flags -e, -t or -a to determine the desired precision(s) of the calculation.')

		parser.add_argument('-b', '--binary', dest='binary', action='store_const', const=True, default=False, help='Inputs D and N are seen as exponents with base 2')
		parser.add_argument('-c', '--combinations', dest='combinations', action='store_const', const=True, default=False, help="Input D is seen as a number of unique items in a set from which we can yield N! (factorial) different members for the resulting set of unique items from which we sample. The calculation of D! uses Stirling's approximation which might introduce a small error responsible for the difference in results with the same input with and without -c flag.")

		parser.add_argument('-t', '--taylor', dest='taylor', action='store_const', const=True, default=False, help='Use Taylor approximation to calculate the birthday problem (best suited for extremely large numbers)')
		parser.add_argument('-s', '--stirling', dest='stirling', action='store_const', const=True, default=False, help='Use exact method but approximate faculty calculations with Stirling\'s formula (only with flag -n) (best suited up to extremely large numbers)')
		parser.add_argument('-e', '--exact', dest='exact', action='store_const', const=True, default=False, help='Use exact method (WARNING! This method becomes too slow very quickly as calculations grow with complexity O(N!) where N is the size of the sampled set) (best suited for smaller numbers)')
		parser.add_argument('-a', '--all', dest='all', action='store_const', const=True, default=False, help='Use all methods for the calculation (same as using flags -e, -s, -t when used with -n, otherwise same as using flags -e, -t)')

		parser.add_argument('-j', '--json', dest='json', action='store_const', const=True, default=False, help='Output results as a Json object')

		parser.add_argument('--prec', dest='prec', action='store', default=10, type=int, help='The number of digits (at most) to the right of the decimal point, where applicable, in the answer (a number between 0 and 10, default is 10)')

		args = parser.parse_args(args) if args is not None else parser.parse_args()

		if args.probability is None and args.samples is None:
			parser.error("Please provide one of flags -n or -p with corresponding argument.")
		elif args.probability is not None and args.samples is not None:
			parser.error("Please provide EITHER a flag -n or -p, not both.")
		elif not args.stirling and not args.exact and not args.taylor and not args.all:
			parser.error("Must set at least one of flags -s, -t, -e or -a.")
		elif (args.stirling) and args.samples is None:
			parser.error("Flag -s should only be used with flag -n.")
		elif (args.stirling or args.exact or args.taylor) and args.all:
			parser.error("Flag -a was set and implicitly includes -s (with -n), -t and -e which should then not be used.")
		elif re.fullmatch(r'[\d]+', args.d[0]) is None:
			parser.error("Illegal input for D: please provide a non-negative integer with digits only")
		elif args.samples and re.fullmatch(r'[\d]+', args.samples) is None:
			parser.error("Illegal input for N: please provide a non-negative integer with digits only")
		elif args.probability and re.fullmatch(r'(1\.[0]+|0\.[\d]+)', args.probability) is None:
			parser.error("Illegal input for P: please provide a non-negative decimal number in the range [0.0, 1.0]")
		elif args.prec < 0 or args.prec > 10:
			parser.error("Illegal input for prec: please provide an integer number in the range [0, 10]")

		return (args.d[0], args.samples, args.probability, args.binary, args.combinations, args.stirling, args.taylor, args.exact, args.all, args.json, args.prec)

class _BirthdayProblemCLISolver:

	########################################################################################################################################################################################################
	########################################################################################################################################################################################################
	#																																																	   #
	#	Solver for standalone use from the command line. Output to the commandline in program form or in Json form for other UIs.																		   #
	#																																																	   #
	########################################################################################################################################################################################################
	########################################################################################################################################################################################################

	@staticmethod
	def __setup(args = None, varMap = {}):
		_DecimalContext.reset()
		dOrDLog, nOrNLog, p, isBinary, isCombinations, isStirling, isTaylor, isExact, isAll, isJson, prec = _BirthdayProblemInputParser.parse(args)
		dOrDLog = Decimal(dOrDLog)
		nOrNLog = None if nOrNLog is None else Decimal(nOrNLog)
		p = None if p is None else Decimal(p)

		_BirthdayProblemInputHandler.sanitize(dOrDLog, nOrNLog, p, isBinary, isCombinations, isStirling, isTaylor, isExact, isAll, varMap)
		d, dLog, n, nLog, p = _BirthdayProblemInputHandler.setup(dOrDLog, nOrNLog, p, isBinary, isCombinations)

		return  d, dLog, n, nLog, p, _DecimalFns.toPercent(p) if p is not None else None, isBinary, isStirling, isTaylor, isExact, isAll, isJson, prec

	@staticmethod
	def solve(args = None):
		isMainProgram = args is None
		try:
			varMap = {}
			if(isMainProgram):
				varMap = { "dOrDLog": "D", "nOrNLog": "N", "p": "probability", "isBinary": "binary", "isCombinations": "combinations", "isStirling": "stirling", "isTaylor": "taylor", "isExact": "exact", "isAll": "all" }
			d, dLog, n, nLog, p, pPercent, isBinary, isStirling, isTaylor, isExact, isAll, isJson, prec = _BirthdayProblemCLISolver.__setup(args, varMap)

			if(dLog is None or dLog.as_tuple()[2] > 0): # implies the precision was not enough to store the size of this number, a scale had to be used
				raise SolverException(SolverErrorCode.DLOG_NOT_CALCULATED, message = "couldn't setup calculations because input numbers were too large: the log of the resulting input set size D must not exceed 1000 digits.")
			if(not isBinary and (d is None or d.as_tuple()[2] > 0)): # implies the precision was not enough to store the size of this number, a scale had to be used
				raise SolverException(SolverErrorCode.D_NOT_CALCULATED, message = "couldn't setup calculations because input numbers were too large: the input set size D must not exceed 1000 digits.")
			if(isJson):
				return _BirthdayProblemCLISolver.solveJson(d, dLog, n, nLog, p, pPercent, isBinary, isStirling, isTaylor, isExact, isAll, prec, isMainProgram)
			else:
				return _BirthdayProblemCLISolver.solveText(d, dLog, n, nLog, p, pPercent, isBinary, isStirling, isTaylor, isExact, isAll, prec, isMainProgram)

		except BaseException as e:
			if(isMainProgram):
				print("Failed due to error:", e, file=sys.stderr)
				traceback.print_exception(*sys.exc_info())
				sys.exit(int(e.code) if isinstance(e, SolverException) else 1)
			else:
				raise e

	@staticmethod
	def solveText(d, dLog, n, nLog, p, pPercent, isBinary, isStirling, isTaylor, isExact, isAll, prec, isMainProgram):
		res = []
		outputter = (lambda s: print(s)) if isMainProgram else (lambda s: res.append(s))

		lastMethodUsed = None
		results = []

		# do the calculations based on mode
		if p is not None:
			outputter(_BirthdayProblemTextFormatter.headerTextBirthdayProblemInv(dLog if isBinary else d, p, pPercent, isBinary, prec))
			for (method, included) in [(_BirthdayProblemSolver.CalcPrecision.EXACT, isExact), (_BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX, isTaylor)]:
				if (included or isAll) and lastMethodUsed != _BirthdayProblemSolver.CalcPrecision.TRIVIAL:
					try:
						(n, methodUsed) = _BirthdayProblemSolverChecked.birthdayProblemInv(d, dLog, p, method, isBinary)
						lastMethodUsed = methodUsed
					except BaseException as e:
						methodText = _BirthdayProblemTextFormatter.parenthesize(_BirthdayProblemTextFormatter.methodToShortDescription(method))
						errorText = " (Calculation failed: " + str(e).lower() + methodText + ")"
						if isinstance(e, KeyboardInterrupt):
							results += [("N/A", "", " (Interrupted by user" + methodText + ")")]
						elif isinstance(e, SolverException):
							results += [("N/A", "", errorText)]
						else:
							results += [("N/A", "", errorText)]
					else:
						results += [_BirthdayProblemTextFormatter.resultTextBirthdayProblemInv(n, isBinary, methodUsed, prec)]
		else:
			outputter(_BirthdayProblemTextFormatter.headerTextBirthdayProblem(dLog if isBinary else d, nLog if isBinary else n, isBinary, prec))
			for (method, included) in [(_BirthdayProblemSolver.CalcPrecision.EXACT, isExact), (_BirthdayProblemSolver.CalcPrecision.STIRLING_APPROX, isStirling), (_BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX, isTaylor)]:
				if (included or isAll) and lastMethodUsed != _BirthdayProblemSolver.CalcPrecision.TRIVIAL:
					try:
						(p, methodUsed) = _BirthdayProblemSolverChecked.birthdayProblem(d, dLog, n, nLog, method, isBinary)
						lastMethodUsed = methodUsed
						pPercent = _DecimalFns.toPercent(p)
					except BaseException as e:
						methodText = _BirthdayProblemTextFormatter.parenthesize(_BirthdayProblemTextFormatter.methodToShortDescription(method))
						errorText = " (Calculation failed: " + str(e).lower() + methodText + ")"
						if isinstance(e, KeyboardInterrupt):
							results += [("N/A", "", " (Interrupted by user" + methodText + ")")]
						elif isinstance(e, SolverException):
							results += [("N/A", "", errorText)]
						else:
							results += [("N/A", "", errorText)]
					else:
						results += [_BirthdayProblemTextFormatter.resultTextBirthdayProblem(p, pPercent, methodUsed, prec)]
		# map every value for results and log10 results to the length of the string (=> an array of tuples), then spread it with * so that we add tuples as vararg input to zip which will then create two
		# lists, one with all first value, and one with all last values. For each of these arrays, we take the maximum and then we have the length of the longest res text and the length of the longest log 10 res text
		(maxLenRes, maxLenLog10Repr) = map(lambda l: max(l), zip(*map(lambda tup: (len(tup[0]), len(tup[1])), results)))
		for (resText, log10Repr, methodText) in results:
			outputter(_BirthdayProblemTextFormatter.indented(resText.ljust(maxLenRes, " ") +  log10Repr.ljust(maxLenLog10Repr, " ") + methodText))
		if(not isMainProgram):
			return "\n".join(res)

	@staticmethod
	def solveJson(d, dLog, n, nLog, p, pPercent, isBinary, isStirling, isTaylor, isExact, isAll, prec, isMainProgram):
		res = {'results': {}}

		# do the calculations based on mode
		if p is not None:
			dText, pText = _BirthdayProblemTextFormatter.headerTextBirthdayProblemInvNumbers(dLog if isBinary else d, p, pPercent, isBinary, prec)
			res['d'] = dText
			res['p'] = pText
			lastMethodUsed = None
			for (method, included) in [(_BirthdayProblemSolver.CalcPrecision.EXACT, isExact), (_BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX, isTaylor)]:
				if (included or isAll) and lastMethodUsed != _BirthdayProblemSolver.CalcPrecision.TRIVIAL:
					try:
						(n, methodUsed) = _BirthdayProblemSolverChecked.birthdayProblemInv(d, dLog, p, method, isBinary)
						lastMethodUsed = methodUsed
					except BaseException as e:
						methodKey = _BirthdayProblemTextFormatter.methodToText(_BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX).lower()
						errorMessage = str(e).lower()
						if isinstance(e, KeyboardInterrupt):
							res['results'][methodKey] = { 'error': 'interrupted' }
						elif isinstance(e, SolverException):
							res['results'][methodKey] = { 'error': errorMessage }
						else:
							res['results'][methodKey] = { 'error': errorMessage }
					else:
						methodKey = _BirthdayProblemTextFormatter.methodToText(methodUsed).lower()
						n = "".join(_BirthdayProblemTextFormatter.resultTextBirthdayProblemInvNumbers(n, isBinary, prec))
						res['results'][methodKey] = { 'result' : n }
		else:
			dText, nText  = _BirthdayProblemTextFormatter.headerTextBirthdayProblemNumbers(dLog if isBinary else d, nLog if isBinary else n, isBinary, prec)
			res['d'] = dText
			res['n'] = nText
			lastMethodUsed = None
			for (method, included) in [(_BirthdayProblemSolver.CalcPrecision.EXACT, isExact), (_BirthdayProblemSolver.CalcPrecision.STIRLING_APPROX, isStirling), (_BirthdayProblemSolver.CalcPrecision.TAYLOR_APPROX, isTaylor)]:
				if (included or isAll) and lastMethodUsed != _BirthdayProblemSolver.CalcPrecision.TRIVIAL:
					try:
						(p, methodUsed) = _BirthdayProblemSolverChecked.birthdayProblem(d, dLog, n, nLog, method, isBinary)
						lastMethodUsed = methodUsed
						pPercent = _DecimalFns.toPercent(p)
					except BaseException as e:
						methodKey = _BirthdayProblemTextFormatter.methodToText(method).lower()
						errorMessage = str(e).lower()
						if isinstance(e, KeyboardInterrupt):
							res['results'][methodKey] = { 'error': 'interrupted' }
						elif isinstance(e, SolverException):
							res['results'][methodKey] = { 'error': errorMessage }
						else:
							res['results'][methodKey] = { 'error': errorMessage }
					else:
						methodKey = _BirthdayProblemTextFormatter.methodToText(methodUsed).lower()
						p = "".join(_BirthdayProblemTextFormatter.resultTextBirthdayProblemNumbers(p, pPercent, prec))
						res['results'][methodKey] = { 'result': p }
		res = json.dumps(res)
		if(isMainProgram):
			print(res)
		else:
			return res

# wrapper class that is the actual entry point to all functionality of this class. Only default import
class BirthdayProblem:
	Solver = _BirthdayProblemSolver
	CLISolver = _BirthdayProblemCLISolver

if __name__ == "__main__":
	BirthdayProblem.CLISolver.solve()
