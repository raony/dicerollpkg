import unittest
import mock

from diceroll import DiceRoll

@mock.patch('random.randint')
class DiceRollTest(unittest.TestCase):
    def test_1d10(self, randint_call):
        roll_result = 9
        randint_call.return_value = roll_result

        target = DiceRoll(1, 10)
        result = target.roll()
        self.assertEquals(1, len(result.rolls))
        self.assertEquals(roll_result, result.rolls[0])

    def test_2d10(self, randint_call):
        roll_result = [1, 7]
        randint_call.side_effect = roll_result

        target = DiceRoll(2, 10)
        result = target.roll()

        self.assertEquals(roll_result, result.rolls)

    def test_0d10(self, randint_call):
        target = DiceRoll(0, 10)
        result = target.roll()

        self.assertEquals([], result.rolls)

    def test_10d0(self, randint_call):
        try:
            target = DiceRoll(10, 0)
            self.fail('should raise ValueError')
        except ValueError:
            pass

    def test_1dfraction(self, randint_call):
        target = DiceRoll(1, 6.7)
        self.assertEquals(6, target.dice_type)

    def test_1d10e10_not_exploding(self, randint_call):
        randint_call.return_value = 6
        target = DiceRoll(1, 10, explode_on=[10])
        self.assertEquals(1, len(target.roll().rolls))

    def test_1d10e10_exploding(self, randint_call):
        randint_call.side_effect = [10, 10, 5]
        target = DiceRoll(1, 10, explode_on=[10])
        self.assertEquals(3, len(target.roll().rolls))
