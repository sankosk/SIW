# -*- encoding:utf-8 -*-

# Estos test se ejecutan con el siguiente comando:
#    python -m unittest discover -v
# en la carpeta donde esta este fichero

from __future__ import print_function
#from __future__ import unicode_literals
from __future__ import division

import unittest

# MODIFICAR EL NOMBRE DEL PAQUETE
from bag_of_words_pruebas import BagOfWords, coef_dice, coef_jaccard, coef_cosine, coef_overlapping


class TestBagOfWords(unittest.TestCase):

    def test_init_with_str(self):
        self.assertDictEqual(BagOfWords("cat dog cow").values, {"cat": 1, "dog": 1, "cow": 1})
        self.assertDictEqual(BagOfWords(text="Cat dog cat").values, {"cat": 2, "dog": 1})


    def test_init_with_dict(self):
        self.assertDictEqual(BagOfWords(values={"cat": 1, "dog": 1, "cow": 1}).values, {"cat": 1, "dog": 1, "cow": 1})
        self.assertDictEqual(BagOfWords(values={"cat": 2, "dog": 1}).values, {"cat": 2, "dog": 1})


    def test_init_with_symbols_in_str(self):
        self.assertDictEqual(BagOfWords(" cat, dog! cow.").values, {"cat": 1, "dog": 1, "cow": 1})
        self.assertDictEqual(BagOfWords(text="cat dog?? cat!!! ").values, {"cat": 2, "dog": 1})

    def test_str(self):
        txt = str(BagOfWords("cat dog cow"))
        self.assertTrue(txt.startswith("{"))
        self.assertIn("'cat': 1", txt)
        self.assertIn("'dog': 1", txt)
        self.assertIn("'cow': 1", txt)
        self.assertTrue(txt.endswith("}"))

    def test_len(self):
        self.assertEqual(len(BagOfWords()), 0)
        self.assertEqual(len(BagOfWords("cat dog cow")), 3)
        self.assertEqual(len(BagOfWords(text="cat dog cat")), 2)

    def test_iter(self):
        self.assertSequenceEqual(sorted(iter(BagOfWords())), [])
        self.assertSequenceEqual(sorted(iter(BagOfWords("cat cow dog"))), [("cat", 1), ("cow", 1), ("dog", 1)])
        self.assertSequenceEqual(sorted(iter(BagOfWords(text="cat dog cat"))), [("cat", 2), ("dog", 1)])

    def test_intersection(self):
        bag1 = BagOfWords("cat dog cow fish cat cat fish")
        bag2 = BagOfWords("dog grape banana peach")
        self.assertDictEqual(bag1.intersection(bag2).values, {"dog": 1})

    def test_union(self):
        bag1 = BagOfWords("cat dog cow fish cat cat fish")
        bag2 = BagOfWords("dog grape banana peach")
        self.assertDictEqual(bag1.union(bag2).values, {"banana": 1, "cat": 3, "cow": 1, "dog": 2, "fish": 2, "grape": 1, "peach": 1})


class TestCoefs(unittest.TestCase):

    def test_coef_dice(self):
        bag1 = BagOfWords("cat dog cow fish cat cat fish")
        bag2 = BagOfWords("dog grape banana cat")
        self.assertAlmostEqual(coef_dice(bag1, bag2), 0.5)

    def test_coef_jaccard(self):
        bag1 = BagOfWords("cat dog cow fish cat cat fish")
        bag2 = BagOfWords("dog grape banana cat")
        self.assertAlmostEqual(coef_jaccard(bag1, bag2), 0.333, places=3)

    def test_coef_cosine(self):
        bag1 = BagOfWords("cat dog cow fish cat cat fish")
        bag2 = BagOfWords("dog grape banana cat")
        self.assertAlmostEqual(coef_cosine(bag1, bag2), 0.125)

    def test_coef_overlapping(self):

        bag1 = BagOfWords("cat dog cow fish cat cat fish")
        bag2 = BagOfWords("dog grape banana cat")
        self.assertAlmostEqual(coef_overlapping(bag1, bag2), 0.5)


if __name__ == '__main__':
    unittest.main()
