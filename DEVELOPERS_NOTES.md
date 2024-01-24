
* `Decimal`'s are immutable but in some places, an input is wrapped in `Decimal(x)`. This is likely because this input
  can sometimes be a regular number OR has been so historically and the creation of a `Decimal` has been left.
* Adjustments of `Decimal`'s via `adjustPrecisions` is an attempt to allow a certain number of decimals to the right of 
  the comma so that, depending on the integer part, a `Decimal` can have its precision increased or decreased at 
  different times after some processing has been done. If this results in a too big number, then the precision needed is 
  too big and we can't carry out the calculations. This limit is set at 1000 digits (out of which 100 at most are to the
  right of the comma). Larger numbers than this will result in the calculations failing.
