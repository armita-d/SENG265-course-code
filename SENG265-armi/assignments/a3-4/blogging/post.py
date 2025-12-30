'''
defines the Post class for individual blog posts.

each post has a unique code, title, text, creation time and last update time


'''
from datetime import datetime

#initialize a Post obj with code , title, and text
class Post:
    def __init__(self,code, title, text):
        self.code = code #will be set by Blog
        self.title = title
        self.text = text
        self.creation = datetime.now()
        self.update = self.creation

#defie equality between two Post objects based on code, title and text
    def __eq__(self, other):
        if not isinstance(other, Post):
            return NotImplemented
        return (self.code == other.code and
                self.title == other.title and
                self.text == other.text)

#string represntation for printing a Post obj
    def __str__(self):
        return f"Post #{self.code}: {self.title}"

#detailed represntation for debugging purpose
    def __repr__(self):
        return f"Post(code={self.code}, title='{self.title}', text='{self.text}')"
