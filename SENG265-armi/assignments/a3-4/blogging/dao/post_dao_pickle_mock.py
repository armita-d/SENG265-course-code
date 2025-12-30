from datetime import datetime
from blogging.post import Post # Needed for object storage

class PostDAOPickle:
    # 1. CRITICAL FIX: The constructor MUST be _init_ and accept blog_instance
    def __init__(self, blog_instance):
        # The Blog object passed by the controller/Blog model
        self.blog = blog_instance
        
        # Internal storage for posts (mimicking the file content)
        self.posts = {}
        
        # Ensures the counter starts/restarts correctly for tests
        # The real DAO loads this from the file, but here we hardcode the start.
        self.blog.next_post_code = 1 

    # --- CRUD Operations ---

    def create_post(self, post):
        """Mocks post creation: assigns a code and stores it in memory."""
        post_code = self.blog.next_post_code
        
        # Assign the generated code back to the Post object
        post.code = post_code 
        
        # Store in mock memory
        self.posts[post_code] = post
        
        # Increment the counter
        self.blog.next_post_code += 1
        return post

    def search_post(self, post_code):
        """Mocks searching for a single post by code."""
        return self.posts.get(post_code)

    def retrieve_posts(self, search_text):
        """Mocks searching posts by text (for 'test_retrieve_posts')."""
        normalized_search = search_text.lower()
        found_posts = []
        for post in self.posts.values():
            if normalized_search in post.title.lower() or normalized_search in post.text.lower():
                found_posts.append(post)
        return found_posts

    def update_post(self, post_code, new_title, new_text):
        """Mocks updating a post; returns the updated post or None."""
        if post_code in self.posts:
            post = self.posts[post_code]
            post.title = new_title
            post.text = new_text
            post.update = datetime.now() # Mock update timestamp
            return post
        return None

    def delete_post(self, post_code):
        """Mocks deleting a post; returns True for success, False otherwise."""
        if post_code in self.posts:
            del self.posts[post_code]
            return True
        return False

    def list_posts(self):
        """Mocks listing all posts, sorted by code descending."""
        all_posts = list(self.posts.values())
        all_posts.sort(key=lambda post: post.code, reverse=True)
        return all_posts
