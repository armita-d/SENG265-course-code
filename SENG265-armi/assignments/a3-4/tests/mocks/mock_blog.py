#tests/mock_blog.py
from blogging.post import Post

class MockBlog:
    def __init__(self):
        self.posts = []
        self._next_post_id = 1

    def add_post(self, title, content):
        post = Post(title, content)
        post.id = self._next_post_id
        self._next_post_id += 1
        self.posts.append(post)
        return post


    def get_posts(self):
        return sorted(self.posts, key=lambda x: x.creation, reverse = True)

    def get_post(self, post_id):
        for post in self.posts:
            if post.id == post_id:
                return post
        return None
