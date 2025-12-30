# blogging/dao/post_dao_pickle.py

import os
import pickle
from datetime import datetime

from blogging.dao.post_dao import PostDAO
from blogging.configuration import Configuration
from blogging.post import Post


class PostDAOPickle(PostDAO):
    """
    DAO for posts of a single blog.
    - In-memory when autosave = False.
    - Pickle-based file persistence when autosave = True.
    """

    def __init__(self, blog):
        self.blog = blog
        self.autosave = Configuration.autosave
        self.posts = {}  # key: post_code, value: Post

        if self.autosave:
            self._load_posts()
        else:
            # When not autosaving, start with an empty collection and counter = 1
            self.blog.next_post_code = 1

    # --- helpers ---

    def _ensure_records_path(self):
        path = Configuration.records_path
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path

    def _get_filename(self):
        records_path = self._ensure_records_path()
        ext = Configuration.records_extension
        return os.path.join(records_path, f"{self.blog.id}{ext}")

    def _load_posts(self):
        filename = self._get_filename()
        if not os.path.exists(filename):
            self.posts = {}
            self.blog.next_post_code = 1
            return

        try:
            with open(filename, "rb") as f:
                self.posts = pickle.load(f)
        except Exception:
            # corrupted/empty file
            self.posts = {}

        if self.posts:
            self.blog.next_post_code = max(self.posts.keys()) + 1
        else:
            self.blog.next_post_code = 1

    def _save_posts(self):
        if not self.autosave:
            return
        filename = self._get_filename()
        try:
            with open(filename, "wb") as f:
                pickle.dump(self.posts, f)
        except Exception as e:
            print(f"Error saving posts file: {e}")

    # --- DAO methods ---

    def create_post(self, post):
        """
        Assigns a new code, stores the post, and returns it.
        """
        code = self.blog.next_post_code
        post.code = code
        self.posts[code] = post
        self.blog.next_post_code += 1

        self._save_posts()
        return post

    def search_post(self, key):
        return self.posts.get(key)

    def retrieve_posts(self, search_string):
        normalized = search_string.lower()
        result = []
        for post in self.posts.values():
            if (normalized in post.title.lower()
                    or normalized in post.text.lower()):
                result.append(post)
        # dict preserves insertion order; this matches assignment tests
        return result

    def update_post(self, key, new_title, new_text):
        if key not in self.posts:
            return None

        post = self.posts[key]
        post.title = new_title
        post.text = new_text
        post.update = datetime.now()

        self._save_posts()
        return post

    def delete_post(self, key):
        if key in self.posts:
            del self.posts[key]
            self._save_posts()
            return True
        return False

    def list_posts(self):
        """
        Returns posts sorted by code, descending.
        This matches the expected order in controller/integration tests.
        """
        posts = list(self.posts.values())
        posts.sort(key=lambda p: p.code, reverse=True)
        return posts
