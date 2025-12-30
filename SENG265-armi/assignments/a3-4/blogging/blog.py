from blogging.post import Post
from blogging.dao.post_dao_pickle import PostDAOPickle
class Blog:
    def __init__(self, id,name, url, email):
        self.id = id
        self.name = name
        self.url = url
        self.email = email

        self.next_post_code = 1
        self.post_dao = PostDAOPickle(self)

    def __eq__(self, other):
        if not isinstance(other, Blog):
            return NotImplemented
        return (self.id == other.id and
                self.name == other.name and
                self.url == other.url and
                self.email == other.email
        )

    def __str__(self):
        return f"Blog #{self.id}: {self.name}"

    def __repr__(self):
        return f"Blog(id={self.id}, name='{self.name}', url='{self.url}', email='{self.email}')"

    def update_details(self, new_name=None, new_url=None,new_email=None):
        if new_name is not None:
            self.name = new_name
        if new_url is not None:
            self.url = new_url
        if new_email is not None:
            self.email = new_email
        return True
    #Story 10
    def create_post(self, title, text):
        new_post = Post(None, title, text)
        return self.post_dao.create_post(new_post)

    #Story 11
    def retrieve_posts_by_text(self, search_text):
        return self.post_dao.retrieve_posts(search_text)

        for post in self.posts.values():
            if normalized_search in post.title.lower() or normalized_search in post.text.lower():
                found_posts.append(post)
        return found_posts
    
    #Story 12
    def update_post(self,post_code, new_title, new_text):
        return self.post_dao.update_post(post_code, new_title, new_text)
    
    #Story 13
    def delete_post(self, post_code):
        return self.post_dao.delete_post(post_code)
    
    #Story 14
    def list_all_posts(self):
        return self.post_dao.list_posts()
    
    def search_post(self, post_code):
        return self.post_dao.search_post(post_code)
