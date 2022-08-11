import unittest

from utils.utils import get_string_from_file


class TestUtils(unittest.TestCase):
    def test_get_string_from_file(self):
        expected = "This is line one,\nthis is line two,\nthis is line three"
        actual = get_string_from_file("resources/lines.txt")
        self.assertEqual(expected, actual, "Strings aren't equal")


if __name__ == '__main__':
    unittest.main()
