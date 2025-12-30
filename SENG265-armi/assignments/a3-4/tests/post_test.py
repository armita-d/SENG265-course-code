'''
tests cover initialization , equality and string/represantation methods.
'''
import unittest
from datetime import datetime
from blogging.post import Post
from blogging.blog import Blog

class TestPost(unittest.TestCase):
    def setUp(self): # set up a sample post before each test

        self.post = Post(1,"Test Title", "Test content")

#test initialization and timestamps

    def test_initialization(self):
        self.assertIsNotNone(self.post.creation)
        self.assertEqual(self.post.creation,self.post.update)

#test equality of 2 posts with same fields
    def test_equality_same_fields(self):
        other = Post(1,"Test Title", "Test content")
        self.assertEqual(self.post, other)

#test inequality of posts with diffrent codes
    def test_equality_different_code(self):
        other = Post(2,"Test Title", "Test content")
        self.assertNotEqual(self.post,other)

#test string represntation
    def test_str_representation(self):
        s = str(self.post)
        self.assertIn("Post #1", s)
        self.assertIn("Test Title", s)

#test repr method
    def test_repr_contains_all_fields(self):
        r = repr(self.post)
        self.assertIn("Post(code=1",r)
        self.assertIn("Test Title",r)
        self.assertIn("Test content",r)

if __name__ =="__main__":
    unittest.main()
