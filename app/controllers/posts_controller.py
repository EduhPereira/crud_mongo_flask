from flask import Flask, jsonify, request
from app.exceptions.posts_exceptions import InvalidPostError
from app.models.post_model import Post

def init_app(app: Flask):

    @app.get('/posts')
    def get_all_posts():
        posts_list = Post.get_all()
        return jsonify(posts_list)


    @app.get('/posts/<int:post_id>')
    def get_one_post(post_id):
        try:
            post = Post.get_one(post_id)
            return post
        except TypeError:
            return {"message":"post not found"},404

    
    @app.post('/posts')
    def create_post():

        data = request.json

        try:
            post = Post(**data)
            new_post = post.save()
            return new_post, 201
        except (InvalidPostError, TypeError):
            return {'message': 'invalid data to create a post'}, 400
    

    @app.patch('/posts/<int:post_id>')
    def update_one_post(post_id):
        try:
            data = request.json
            post = Post.update_one(post_id, data)
        except TypeError:
            return{"message":"invalid data to update a post"},404
        return {"post updated":post},200

    @app.delete('/posts/<int:post_id>')
    def delete_one_post(post_id):
        result = Post.delete_one(post_id)
        if result[0] == 0:
            return {"message":"post not found to be deleted"},404
        return {"post deleted":result[1]},200
