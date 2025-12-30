# blogging/controller.py

"""
Defines the Controller class that manages blogs, posts and user authentication.
Supports login/logout, blog creation, update, deletion, post management,
and search functions.
"""

import hashlib

from blogging.blog import Blog
from blogging.dao.blog_dao_json import BlogDAOJSON
from blogging.configuration import Configuration

# Exception imports
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


def hash_password(password):
    """Creates a SHA-256 hash digest of a given password."""
    return hashlib.sha256(password.encode()).hexdigest()


class Controller:
    def __init__(self):
        # Respect global configuration flag
        self.autosave = Configuration.autosave

        self.blog_dao = BlogDAOJSON()

        self.current_user = None
        self.current_blog = None

        self.user_credentials = {}

        if self.autosave:
            self._load_users()
        else:
            # Hardcoded list for controller tests (autosave=False)
            self.user_credentials = {
                "user": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
                "ali": "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810",
                "kala": "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e",
            }

    # --- Users / login ---

    def _load_users(self):
        users_file_path = Configuration.users_file
        try:
            with open(users_file_path, "r") as file:
                for line in file:
                    if line.strip():
                        username, hashed_password = line.strip().split(",")
                        self.user_credentials[username] = hashed_password
        except FileNotFoundError:
            # If missing, just keep empty credentials dict
            pass
        except Exception as e:
            print(f"Error loading users file: {e}")

    def login(self, username, password):
        if self.current_user is not None:
            raise DuplicateLoginException("User already logged in.")

        hashed = hash_password(password)
        if (
            username not in self.user_credentials
            or self.user_credentials[username] != hashed
        ):
            raise InvalidLoginException("Invalid username or password.")

        self.current_user = username
        return True

    def logout(self):
        if self.current_user is None:
            raise InvalidLogoutException("No user is currently logged in.")

        self.current_user = None
        self.current_blog = None
        return True

    # --- Blogs ---

    def create_blog(self, blog_id, name, url, email):
        if self.current_user is None:
            raise IllegalAccessException("Cannot create blog without logging in.")

        if self.blog_dao.search_blog(blog_id) is not None:
            raise IllegalOperationException(
                f"Blog with ID {blog_id} already exists."
            )

        new_blog = Blog(blog_id, name, url, email)
        return self.blog_dao.create_blog(new_blog)

    def search_blog(self, blog_id):
        if self.current_user is None:
            raise IllegalAccessException("Cannot search blog without logging in.")
        return self.blog_dao.search_blog(blog_id)

    def retrieve_blogs(self, search_name):
        if self.current_user is None:
            raise IllegalAccessException("Cannot retrieve blogs without logging in.")
        return self.blog_dao.retrieve_blogs(search_name)

    def list_blogs(self):
        if self.current_user is None:
            raise IllegalAccessException("Cannot list blogs without logging in.")
        return self.blog_dao.list_blogs()

    def update_blog(self, old_id, new_id, new_name, new_url, new_email):
        if self.current_user is None:
            raise IllegalAccessException("Cannot update blog without logging in.")

        # Cannot update the current blog
        if self.current_blog is not None and self.current_blog.id == old_id:
            raise IllegalOperationException("Cannot update the current blog.")

        # Old blog must exist
        if self.blog_dao.search_blog(old_id) is None:
            raise IllegalOperationException(
                f"Blog with ID {old_id} not registered."
            )

        # New ID cannot conflict
        if new_id != old_id and self.blog_dao.search_blog(new_id) is not None:
            raise IllegalOperationException(
                f"New ID {new_id} conflicts with an existing blog ID."
            )

        return self.blog_dao.update_blog(
            old_id, new_id, new_name, new_url, new_email
        )

    def delete_blog(self, blog_id):
        if self.current_user is None:
            raise IllegalAccessException("Cannot delete blog without logging in.")

        if self.blog_dao.search_blog(blog_id) is None:
            raise IllegalOperationException(
                f"Blog with ID {blog_id} not registered."
            )

        if self.current_blog and self.current_blog.id == blog_id:
            raise IllegalOperationException("Cannot delete the current active blog.")

        return self.blog_dao.delete_blog(blog_id)

    # --- Current blog management ---

    def set_current_blog(self, blog_id):
        if self.current_user is None:
            raise IllegalAccessException("Cannot set current blog without logging in.")

        blog = self.blog_dao.search_blog(blog_id)
        if blog is None:
            raise IllegalOperationException(
                "Cannot set non-existent blog as the current blog."
            )

        self.current_blog = blog
        return self.current_blog

    def unset_current_blog(self):
        if self.current_user is None:
            raise IllegalAccessException("Cannot unset current blog without logging in.")
        self.current_blog = None
        return True

    def get_current_blog(self):
        if self.current_user is None:
            raise IllegalAccessException("Cannot get current blog without logging in.")
        return self.current_blog

    # --- Posts (delegated to current blog) ---

    def create_post(self, title, text):
        if self.current_user is None:
            raise IllegalAccessException("Cannot create post without logging in.")
        if self.current_blog is None:
            raise NoCurrentBlogException(
                "Cannot create post without a current blog selected."
            )
        return self.current_blog.create_post(title, text)

    def list_posts(self):
        if self.current_user is None:
            raise IllegalAccessException("Cannot list posts without logging in.")
        if self.current_blog is None:
            raise NoCurrentBlogException(
                "Cannot list posts without a current blog selected."
            )
        return self.current_blog.list_all_posts()

    def retrieve_posts(self, text):
        if self.current_user is None:
            raise IllegalAccessException("Cannot retrieve posts without logging in.")
        if self.current_blog is None:
            raise NoCurrentBlogException(
                "Cannot retrieve posts without a current blog selected."
            )
        return self.current_blog.retrieve_posts_by_text(text)

    def update_post(self, post_code, new_title, new_text):
        if self.current_user is None:
            raise IllegalAccessException("Cannot update post without logging in.")
        if self.current_blog is None:
            raise NoCurrentBlogException(
                "Cannot update post without a current blog selected."
            )

        updated = self.current_blog.update_post(post_code, new_title, new_text)
        if updated is None:
            return False
        return True

    def delete_post(self, post_code):
        if self.current_user is None:
            raise IllegalAccessException("Cannot delete post without logging in.")
        if self.current_blog is None:
            raise NoCurrentBlogException(
                "Cannot delete post without a current blog selected."
            )

        success = self.current_blog.delete_post(post_code)
        if not success:
            return False
        return True

    def search_post(self, post_code):
        if self.current_user is None:
            raise IllegalAccessException("Cannot search post without logging in.")
        if self.current_blog is None:
            raise NoCurrentBlogException(
                "Cannot search post without a current blog selected."
            )
        return self.current_blog.search_post(post_code)
