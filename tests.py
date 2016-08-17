import unittest

import mock

from diceroll import DiceRoll, ExplodingDiceRoll, SuccessRollResult, parse, DiceRollResult, validate_dice_pattern, \
    SumRollResult


class validate_dice_pattern_test(unittest.TestCase):
    def test_validate_dice_pattern(self):
        self.assertTrue(validate_dice_pattern('1d10'))
        self.assertTrue(validate_dice_pattern('12d1>2'))
        self.assertTrue(validate_dice_pattern('1d10!'))
        self.assertTrue(validate_dice_pattern('1d10!2>2'))
        self.assertFalse(validate_dice_pattern('d10'))
        self.assertFalse(validate_dice_pattern('1d'))
        self.assertFalse(validate_dice_pattern('1d1!!>'))


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

    def test_result_class(self, randint_call):
        randint_call.return_value = 2
        target = DiceRoll(1, 7, result_class=SuccessRollResult.with_treshold(8))
        result = target.roll()
        self.assertIsInstance(result, SuccessRollResult)

@mock.patch('random.randint')
class ExplodingDiceRollTest(unittest.TestCase):
    def test_1d10e10_not_exploding(self, randint_call):
        randint_call.return_value = 6
        target = ExplodingDiceRoll(1, 10, explode_on=[10])
        self.assertEquals(1, len(target.roll().rolls))

    def test_1d10e10_exploding(self, randint_call):
        randint_call.side_effect = [10, 10, 5]
        target = ExplodingDiceRoll(1, 10, explode_on=[10])
        self.assertEquals(3, len(target.roll().rolls))

    def test_1d6e5_exploding(self, randint_call):
        randint_call.side_effect = [5, 6, 4]
        target = ExplodingDiceRoll(1, 6, explode_on=[5,6])
        self.assertEquals(3, len(target.roll().rolls))

class SumDiceResultTest(unittest.TestCase):
    def test_positive_mod(self):
        target = SumRollResult(None, [1,5,8], 3)
        self.assertEquals(17, target.total)

    def test_negative_mod(self):
        target = SumRollResult(None, [1, 5, 8], -3)
        self.assertEquals(11, target.total)

class SuccessDiceRollTest(unittest.TestCase):
    def test_success(self):
        target = SuccessRollResult(None, [1, 2,7,9,10], 8)
        self.assertEquals(2, target.success())

class ParseRollTest(unittest.TestCase):
    def test_two_digit_roll(self):
        value = parse('10d8>8')
        self.assertEquals(10, value.dices)
        self.assertEquals(8, value.dice_type)
        result = value.roll()
        self.assertIsInstance(result, SuccessRollResult)
        result.success()

    def test_simple_roll(self):
        value = parse('1d6')
        self.assertEquals(1, value.dices)
        self.assertEquals(6, value.dice_type)
        self.assertEquals(DiceRollResult, value._result_class)
        value.roll()

    def test_exploding_roll(self):
        value = parse('1d6!')
        self.assertIsInstance(value, ExplodingDiceRoll)
        self.assertEquals(1, value.dices)
        self.assertEquals(6, value.dice_type)
        self.assertEquals([6], value.explode_on)
        self.assertEquals(DiceRollResult, value._result_class)
        value.roll()

    def test_exploding_different_value(self):
        value = parse('3d6!4')
        self.assertIsInstance(value, ExplodingDiceRoll)
        self.assertEquals(3, value.dices)
        self.assertEquals(6, value.dice_type)
        self.assertEquals([4,5,6], value.explode_on)
        self.assertEquals(DiceRollResult, value._result_class)
        value.roll()

    def test_treshold(self):
        value = parse('3d6>5')
        self.assertEquals(3, value.dices)
        self.assertEquals(6, value.dice_type)
        result = value.roll()
        self.assertIsInstance(result, SuccessRollResult)
        self.assertEquals(5, result.treshold)
        result.success()

    def test_treshold_with_exploding(self):
        value = parse('3d6!>5')
        self.assertEquals(3, value.dices)
        self.assertEquals(6, value.dice_type)
        self.assertEquals([6], value.explode_on)
        result = value.roll()
        self.assertIsInstance(result, SuccessRollResult)
        self.assertEquals(5, result.treshold)
        result.success()

    def test_treshold_with_exploding(self):
        value = parse('3d6!3>5')
        self.assertEquals(3, value.dices)
        self.assertEquals(6, value.dice_type)
        self.assertEquals([3,4,5,6], value.explode_on)
        result = value.roll()
        self.assertIsInstance(result, SuccessRollResult)
        self.assertEquals(5, result.treshold)
        result.success()

    def test_modifier(self):
        value = parse('3d6+5')
        result = value.roll()
        self.assertEquals(5, result.modifier)
        self.assertIsInstance(result, SumRollResult)