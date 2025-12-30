# blogging/dao/blog_dao_json.py

import json
import os

from blogging.dao.blog_dao import BlogDAO
from blogging.configuration import Configuration
from blogging.dao.blog_encoder import BlogEncoder
from blogging.dao.blog_decoder import BlogDecoder


class BlogDAOJSON(BlogDAO):

    def __init__(self):
        self.autosave = Configuration.autosave
        self.blogs = {}  # key: int blog_id, value: Blog

        if self.autosave:
            self._load_blogs()

    def _load_blogs(self):
        blogs_file = Configuration.blogs_file
        if not os.path.exists(blogs_file):
            self.blogs = {}
            return

        try:
            with open(blogs_file, "r") as f:
                raw = json.load(f, cls=BlogDecoder)
                # raw is a dict with string keys and Blog values
                self.blogs = {int(k): v for k, v in raw.items()}
        except json.JSONDecodeError:
            # empty or corrupted file – treat as no blogs
            self.blogs = {}
        except Exception as e:
            print(f"Error loading blogs file: {e}")
            self.blogs = {}

    def _save_blogs(self):
        if not self.autosave:
            return

        blogs_file = Configuration.blogs_file
        try:
            with open(blogs_file, "w") as f:
                # keys (ints) become strings automatically in JSON
                json.dump(self.blogs, f, cls=BlogEncoder, indent=4)
        except Exception as e:
            print(f"Error saving blogs file: {e}")

    # --- CRUD methods (used only via Controller) ---

    def search_blog(self, key):
        return self.blogs.get(key)

    def create_blog(self, blog):
        self.blogs[blog.id] = blog
        self._save_blogs()
        return blog

    def retrieve_blogs(self, search_string):
        normalized = search_string.lower()
        return [
            blog
            for blog in self.blogs.values()
            if normalized in blog.name.lower()
        ]

    # Use slightly richer signature than abstract, but only Controller calls this.
    def update_blog(self, old_id, new_id, new_name, new_url, new_email):
        blog = self.blogs.pop(old_id)

        blog.id = new_id
        blog.update_details(new_name, new_url, new_email)

        self.blogs[new_id] = blog
        self._save_blogs()
        return True

    def delete_blog(self, key):
        if key in self.blogs:
            del self.blogs[key]
            self._save_blogs()
            return True
        return False

    def list_blogs(self):
        # order matters for tests: creation order preserved in dict
        return list(self.blogs.values())
