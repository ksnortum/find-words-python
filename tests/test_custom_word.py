import unittest

from model.custom_word import CustomWord


class TestCustomWord(unittest.TestCase):
    test_word = "punjabi"
    test_value_word = "punjbi"

    def test_custom_word(self):
        this_word = CustomWord(self.test_word, self.test_value_word, False)
        self.assertEqual(self.test_word, this_word.get_word())
        self.assertEqual(self.test_value_word, this_word.get_value_word())
        self.assertEqual(17, this_word.get_value())

    def test_bingo(self):
        this_word = CustomWord(self.test_word, self.test_value_word, True)
        self.assertEqual(self.test_word, this_word.get_word())
        self.assertEqual(self.test_value_word, this_word.get_value_word())
        self.assertEqual(67, this_word.get_value())

    def test_equal_objects(self):
        this_word = CustomWord(self.test_word, self.test_value_word, False)
        that_word = CustomWord(self.test_word, self.test_value_word, False)
        self.assertEqual(this_word, that_word)

    def test_not_equal_objects_bingo(self):
        this_word = CustomWord(self.test_word, self.test_value_word, False)
        that_word = CustomWord(self.test_word, self.test_value_word, True)
        self.assertNotEqual(this_word, that_word)

    def test_not_equal_objects_value_word(self):
        this_word = CustomWord(self.test_word, self.test_value_word, False)
        that_word = CustomWord(self.test_word, self.test_word, False)
        self.assertNotEqual(this_word, that_word)

    def test_not_equal_objects_word(self):
        this_word = CustomWord(self.test_word, self.test_value_word, False)
        that_word = CustomWord(self.test_value_word, self.test_value_word, False)
        self.assertNotEqual(this_word, that_word)


if __name__ == '__main__':
    unittest.main()
