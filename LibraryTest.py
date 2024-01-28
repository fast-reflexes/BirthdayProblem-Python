from BirthdayProblem import BirthdayProblem
from decimal import Decimal, ROUND_CEILING

def testFn(args):
    if "p" in args:
        (res, method) = BirthdayProblem.Solver.solveForN(Decimal(args["dOrDLog"]), Decimal(args["p"]), args["isBinary"], args["isCombinations"], args["method"])
        return (res.quantize(Decimal('0.0000000001')) if(args["isBinary"] is True) else res.to_integral_value(ROUND_CEILING), method)
    else:
        (res, method) =  BirthdayProblem.Solver.solveForP(Decimal(args["dOrDLog"]), Decimal(args["nOrNLog"]), args["isBinary"], args["isCombinations"], args["method"])
        return (res.quantize(Decimal('0.000000000001')), method)

assemblerFn = lambda inp: inp

dividerFn = lambda inp: [inp]

# Add input numbers as strings since floating point imprecision in input to Decimal will otherwise affect the output

testData = [
    [
        { "dOrDLog": "1", "p": "1.0", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("2"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "p": "1.0", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("2"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "p": "0.0", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("1"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "p": "0.0", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("1"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("2"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("2"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1000000000", "p": "0.0000001", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("15"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "1", "nOrNLog": "1", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "nOrNLog": "1", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "nOrNLog": "1", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "nOrNLog": "0", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "nOrNLog": "0", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "nOrNLog": "0", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "nOrNLog": "2", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("1"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "nOrNLog": "2", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("1"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "1", "nOrNLog": "2", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("1"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "69", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("11"), BirthdayProblem.Solver.CalcPrecision.EXACT)
    ],
    [
        { "dOrDLog": "69", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("10"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "83", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("12"), BirthdayProblem.Solver.CalcPrecision.EXACT)
    ],
    [
        { "dOrDLog": "83", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("11"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "1000000000", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("37234"), BirthdayProblem.Solver.CalcPrecision.EXACT)
    ],
    [
        { "dOrDLog": "1000000000", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("37233"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "366", "nOrNLog": "23", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.506323011819"), BirthdayProblem.Solver.CalcPrecision.EXACT)
    ],
    [
        { "dOrDLog": "366", "nOrNLog": "23", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.506315474495"), BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX)
    ],
    [
        { "dOrDLog": "366", "nOrNLog": "23", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.514549326419"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "366", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("23"), BirthdayProblem.Solver.CalcPrecision.EXACT)
    ],
    [
        { "dOrDLog": "366", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("23"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "6274264876827642864872634872364782634", "nOrNLog": "2376287346287353638", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.362366927782"), BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX)
    ],
    [
        { "dOrDLog": "6274264876827642864872634872364782634", "nOrNLog": "2376287346287353638", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.362366927782"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "128", "nOrNLog": "0", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "128", "nOrNLog": "0", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "128", "nOrNLog": "129", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("1"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "128", "nOrNLog": "129", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("1"), BirthdayProblem.Solver.CalcPrecision.TRIVIAL)
    ],
    [
        { "dOrDLog": "128", "nOrNLog": "64", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("0.393469340287"), BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX)
    ],
    [
        { "dOrDLog": "128", "nOrNLog": "64", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("0.393469340287"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "128", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("64.2356168135"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "2000000", "nOrNLog": "1000000", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": True },
        False,
        'needed precision for method exceeds maximum precision'
    ],
    [
        { "dOrDLog": "2000000", "nOrNLog": "1000000", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("0.393469340287"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "2000000", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("1000000.2356168135"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "8", "nOrNLog": "3", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("0.104576930892"), BirthdayProblem.Solver.CalcPrecision.EXACT)
    ],
    [
        { "dOrDLog": "8", "nOrNLog": "3", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("0.104567528314"), BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX)
    ],
    [
        { "dOrDLog": "8", "nOrNLog": "3", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": True },
        True,
        (Decimal("0.117503097415"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "256", "nOrNLog": "8", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.104576930892"), BirthdayProblem.Solver.CalcPrecision.EXACT)
    ],
    [
        { "dOrDLog": "256", "nOrNLog": "8", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.104567528314"), BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX)
    ],
    [
        { "dOrDLog": "256", "nOrNLog": "8", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.117503097415"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "52", "p": "0.1", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": True, "isBinary": False },
        True,
        (Decimal("4119363813276486714957808853108064"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "52", "p": "0.5", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": True, "isBinary": False },
        True,
        (Decimal("10565837726592754214318243269428637"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "52", "nOrNLog": "10000000000000000000", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": True, "isBinary": False },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX)
    ],
    [
        { "dOrDLog": "52", "nOrNLog": "10000000000000000000", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": True, "isBinary": False },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "52", "nOrNLog": "10000000000000000000000000000000000", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": True, "isBinary": False },
        True,
        (Decimal("0.462536366051"), BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX)
    ],
    [
        { "dOrDLog": "52", "nOrNLog": "10000000000000000000000000000000000", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": True, "isBinary": False },
        True,
        (Decimal("0.462536366051"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "4", "nOrNLog": "18", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": True, "isBinary": True },
        True,
        (Decimal("0.001649423866"), BirthdayProblem.Solver.CalcPrecision.EXACT)
    ],
    [
        { "dOrDLog": "4", "nOrNLog": "18", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": True, "isBinary": True },
        True,
        (Decimal("0.001649422224"), BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX)
    ],
    [
        { "dOrDLog": "4", "nOrNLog": "18", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": True, "isBinary": True },
        True,
        (Decimal("0.001649428504"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "16", "nOrNLog": "262144", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": True, "isBinary": False },
        True,
        (Decimal("0.001649423866"), BirthdayProblem.Solver.CalcPrecision.EXACT)
    ],
    [
        { "dOrDLog": "16", "nOrNLog": "262144", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": True, "isBinary": False },
        True,
        (Decimal("0.001649422224"), BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX)
    ],
    [
        { "dOrDLog": "16", "nOrNLog": "262144", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": True, "isBinary": False },
        True,
        (Decimal("0.001649428504"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "20922789888000", "nOrNLog": "262144", "method": BirthdayProblem.Solver.CalcPrecision.EXACT, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.001640861961"), BirthdayProblem.Solver.CalcPrecision.EXACT)
    ],
    [
        { "dOrDLog": "20922789888000", "nOrNLog": "262144", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.001640861961"), BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX)
    ],
    [
        { "dOrDLog": "20922789888000", "nOrNLog": "262144", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": False, "isBinary": False },
        True,
        (Decimal("0.001640868208"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "128", "nOrNLog": "64", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": True, "isBinary": True },
        False,
        'd exceeds maximum size and is needed for method'
    ],
    [
        { "dOrDLog": "128", "nOrNLog": "64", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": True, "isBinary": True },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "1280", "nOrNLog": "640", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": True, "isBinary": True },
        False,
        'd exceeds maximum size and is needed for method'
    ],
    [
        { "dOrDLog": "1280", "nOrNLog": "640", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": True, "isBinary": True },
        True,
        (Decimal("0"), BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX)
    ],
    [
        { "dOrDLog": "12800", "nOrNLog": "6400", "method": BirthdayProblem.Solver.CalcPrecision.STIRLING_APPROX, "isCombinations": True, "isBinary": True },
        False,
        "d exceeds maximum size and is needed for method"
    ],
    [
        { "dOrDLog": "12800", "nOrNLog": "6400", "method": BirthdayProblem.Solver.CalcPrecision.TAYLOR_APPROX, "isCombinations": True, "isBinary": True },
        False,
        "needed precision for method exceeds maximum precision"
    ]
]

