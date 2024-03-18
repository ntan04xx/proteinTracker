import unittest, macros

class test_get_macros(unittest.TestCase):
    def test_nonexistent_food(self):
        with self.assertRaises(ValueError):
            macros.get_macros('13 inch', 'Macbook')
    
    def test_creates_log(self):
        output_food = macros.get_macros('500g', 'chicken breast')
        self.assertTrue(output_food.protein == 112.5)
        self.assertTrue(output_food.calories == 600)
        self.assertTrue(output_food.fat == 13.100000000000001)

if __name__ == '__main__':
    unittest.main()
