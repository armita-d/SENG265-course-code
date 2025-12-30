# blogging/dao/blog_encoder.py

import json
from blogging.blog import Blog

class BlogEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Blog):
            return {
                "__blog__": True,
                "id": obj.id,
                "name": obj.name,
                "url": obj.url,
                "email": obj.email,
            }
        return super().default(obj)
