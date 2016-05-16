import random
import re

class DiceRollResult(object):
    def __init__(self, roll, values):
        self.rolls = values or []
        self.roll = roll

class SuccessRollResult(DiceRollResult):
    def __init__(self, roll, values, treshold):
        super(SuccessRollResult, self).__init__(roll, values)
        self.treshold = treshold

    def success(self):
        return len([x for x in self.rolls if x >= self.treshold])

    @classmethod
    def with_treshold(cls, treshold):
        def wrapper(*args, **kwargs):
            kwargs['treshold'] = treshold
            return SuccessRollResult(*args, **kwargs)
        return wrapper

class DiceRoll(object):
    def __init__(self, dices, dice_type, result_class=DiceRollResult):
        if int(dice_type) <= 1:
            raise ValueError('dice_type should be 1 or greater')
        self.dices = dices
        self.dice_type = int(dice_type)
        self._result_class = result_class

    def _roll(self, dices):
        return [random.randint(1, self.dice_type) for n in xrange(dices)]

    def roll(self):
        return self._result_class(self, self._roll(self.dices))

class ExplodingDiceRoll(DiceRoll):
    def __init__(self, dices, dice_type, result_class=DiceRollResult, explode_on=None):
        super(ExplodingDiceRoll, self).__init__(dices, dice_type, result_class)
        self.explode_on = explode_on or []

    def _roll(self, dices):
        if not dices:
            return []
        result = super(ExplodingDiceRoll, self)._roll(dices)
        exploded = len([x for x in result if x in self.explode_on])
        return result + self._roll(exploded)

    @classmethod
    def with_explode_on(cls, explode_on):
        def wrapper(*args, **kwargs):
            kwargs['explode_on'] = explode_on
            return ExplodingDiceRoll(*args, **kwargs)
        return wrapper

def validate_dice_pattern(pattern):
    return re.match(r'(?P<dices>\d+)d(?P<dice_type>\d+)(?P<explode>!(?P<explode_value>\d+)?)?(?P<treshold>>(?P<treshold_value>\d+))?$', pattern)

def parse(string):
    matches = validate_dice_pattern(string)
    if matches:
        result_class = DiceRollResult
        roll_class = DiceRoll
        dices = int(matches.group('dices'))
        dice_type = int(matches.group('dice_type'))
        if matches.group('explode'):
            explode_value = int(matches.group('explode_value') or dice_type)
            if explode_value < dice_type:
                explode_on = range(explode_value, dice_type+1)
            else:
                explode_on = [dice_type]
            roll_class = ExplodingDiceRoll.with_explode_on(explode_on)
        if matches.group('treshold'):
            treshold = int(matches.group('treshold_value'))
            result_class = SuccessRollResult.with_treshold(treshold)

        return roll_class(dices, dice_type, result_class=result_class)
    raise ValueError('invalid string.')
