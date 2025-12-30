'''
unit test for Blog class using python's unittest framework

test cover blog initalization, post creation, retrieval , updat, deletation 
 and listing
(basiclly the line by line comments gonna be so simmilar to post_test.py so in case of 
confission refer to that.thanks)
'''
import unittest
from datetime import datetime
from blogging.post import Post
from blogging.blog import Blog
class BlogTest(unittest.TestCase):
    def setUp(self): #setup a sample blog before each test
        self.blog = Blog(101,"My travels", "travels.com", "me@travels.com")

#test blog initialization
    def test_initialization(self):
        self.assertEqual(self.blog.id, 101)
        self.assertEqual(self.blog.name, "My travels")
        self.assertEqual(self.blog.url, "travels.com")
        self.assertEqual(self.blog.email, "me@travels.com")
        self.assertEqual(self.blog.next_post_code, 1)
        self.assertEqual(self.blog.posts, {})


    def test_equality_same_fields(self):
        other = Blog(101,"My travels", "travels.com", "me@travels.com")
        self.assertEqual(self.blog, other)
    

    def test_equality_different_url(self):
        other = Blog(101,"My travels", "me.com", "me@travels.com")
        self.assertNotEqual(self.blog,other)

    def test_str_representation(self):
        s = str(self.blog)
        self.assertIn("Blog #101", s)
        self.assertIn("My travels", s)
        
    
    def test_repr_contains_all_fields(self):
        r = repr(self.blog)
        self.assertIn("Blog(id=101", r)
        self.assertIn("My travels", r)
        self.assertIn("travels.com", r)
        self.assertIn("me@travels.com",r)

    def test_create_post(self):
        post1 = self.blog.create_post("Paris 1.0", "Eiffel Tower")
        post2 = self.blog.create_post("Japan has called", "Beauty of Tokya, Mount Fuji")
        self.assertIsInstance(post1, Post)
        self.assertEqual(post1.code,1)
        self.assertEqual(post2.code,2)
        self.assertIn(1,self.blog.posts)
        self.assertIn(2,self.blog.posts)

    def test_list_all_posts(self):
        self.blog.create_post("Post 1", "Text 1")
        self.blog.create_post("Post 2", "Text 2")
        posts = self.blog.list_all_posts()
        self.assertEqual(len(posts),2)
        self.assertEqual(posts[0].code,2)
        self.assertEqual(posts[1].code,1 )
    
    def test_retrieve_posts_by_text(self):
        self.blog.create_post("Paris 1.0", "Eiffel Tower")
        self.blog.create_post("Beautiful Japan has called", "Beauty of Tokya, Mount Fuji")
        results = self.blog.retrieve_posts_by_text("Tower")
        self.assertEqual(len(results),1)
        results = self.blog.retrieve_posts_by_text("beau")
        self.assertEqual(results[0].title, "Beautiful Japan has called")

    def test_update_post(self):
        post = self.blog.create_post("Old Title", "Old text")
        old_update_time = post.update
        updated = self.blog.update_post(1,"New Title", "New text")
        self.assertIsNotNone(updated)
        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.text, "New text")
        self.assertNotEqual(updated.update, old_update_time)

    def text_delete_post(self):
        self.blog.create_post("Post", "To be deleted")
        deleted = self.blog.delete_post(1)
        self.assertTrue(deleted)
        self.assertNotIn(1,self.blog.posts)
        self.assertFalse(self.blog.delete_posts(1))

    def test_update_details(self):
        self.blog.update_details(new_name="Updated Blog", new_url = "updated url")
        self.assertEqual(self.blog.name, "Updated Blog")
        self.assertEqual(self.blog.url, "updated url")
        self.assertEqual(self.blog.email, "me@travels.com")

if __name__ == "__main__":
    unittest.main()
