# dicerollpkg
[![Build Status](https://snap-ci.com/raony/dicerollpkg/branch/master/build_image)](https://snap-ci.com/raony/dicerollpkg/branch/master)

Dice roll package is a simple python package to run dices like:

* 4d6 - will generate 4 rolls of 6 sided dice
* 1d10! - will generate 1 roll of a 10 sided dice that reroll at 10
* 3d8!5 - will generate 3 rolls of a 8 sided dice that reroll if greater or equal to 5
* 1d10!8>8 - will generate 1 roll of a 10 sided dice that reroll if greater or equal to 8 and counts the success as the amount of results greater or equal to 8

## Installing

```
pip install git+https://github.com/raony/dicerollpkg.git
```

## Testing

```
python setup.py test
```