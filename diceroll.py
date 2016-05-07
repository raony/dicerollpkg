import random

class DiceRollResult(object):
    def __init__(self, values):
        self.rolls = values or []

class DiceRoll(object):
    def __init__(self, dices, dice_type, explode_on=None):
        if int(dice_type) <= 1:
            raise ValueError('dice_type should be 1 or greater')
        self.dices = dices
        self.dice_type = int(dice_type)
        self.explode_on = explode_on or []

    def _roll(self, dices):
        if not dices:
            return []
        result = [random.randint(1, self.dice_type) for n in xrange(dices)]
        exploded = len([x for x in result if x in self.explode_on])
        return result + self._roll(exploded)

    def roll(self):
        return DiceRollResult(self._roll(self.dices))

    #     self.roll = self._roll_with_explode(dices)
    #
    # def _roll_with_explode(self, dices):
    #     if not dices:
    #         return []
    #     result = [random.randint(1,10) for n in xrange(dices)]
    #     exploded = len([x for x in result if x == 10])
    #     return result + self._roll_with_explode(exploded)
    #
    # def successes(self):
    #     return len([value for value in self.roll if value >= 8])