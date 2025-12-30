# blogging/dao/blog_decoder.py

import json
from blogging.blog import Blog

class BlogDecoder(json.JSONDecoder):
    """Decodes JSON dictionaries back into Blog objects."""

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        # Matches the structure produced by BlogEncoder
        if "__blog__" in obj:
            return Blog(
                id=obj["id"],
                name=obj["name"],
                url=obj["url"],
                email=obj["email"],
            )
        return obj
