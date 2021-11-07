from flask.json import jsonify
from pymongo import MongoClient
from datetime import datetime
from app.exceptions.posts_exceptions import InvalidPostError


client = MongoClient('mongodb://localhost:27017/')

db = client['kenzie']


class Post():

    allowed_keys = ['created_at', 'update_at', 'title', 'author', 'tags', 'content']

    def __init__(self, title, author, tags, content):
        self.created_at = datetime.now()
        self.update_at = None
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content


    @staticmethod
    def get_all():
        posts_list = list(db.posts.find())
        for post in posts_list:
            del post['_id']
        return posts_list
    
    @staticmethod
    def get_one(post_id):
        post = dict(db.posts.find_one({"id":int(post_id)}))
        del post['_id']
        return post
    
    @staticmethod
    def delete_one(post_id):
        post = dict(db.posts.find_one({"id":int(post_id)}))
        del post['_id']
        result = db.posts.delete_one({"id":int(post_id)})
        return [result.deleted_count, post]
    
    @staticmethod
    def update_one(post_id, data):
        for key in data.keys():
            if not key in Post.allowed_keys:
                raise TypeError
        data['update_at'] = datetime.now()
        db.posts.update_one({'id':int(post_id)}, {'$set':data})
        post = dict(db.posts.find_one({"id":int(post_id)}))
        del post['_id']
        return post

    
    def save(self):
        post = self.__dict__
        post['id'] = int(db.posts.count_documents({})) + 1

        _id = db.posts.insert_one(post).inserted_id

        if not _id:
            raise InvalidPostError
        
        new_post = db.posts.find_one({'_id': _id})

        del new_post['_id']

        return new_post