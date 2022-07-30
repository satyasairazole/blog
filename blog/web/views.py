
from sre_constants import CATEGORY
from unicodedata import category
from flask import Blueprint, redirect, render_template,request,flash,url_for
views=Blueprint('views',__name__)
from flask_login import login_required,current_user
from .models import Post,User,Comments,Likes
from .models import db
@views.route('/home')
@views.route('/')

@login_required
def home():
    post=Post.query.all()
    return render_template('home.html',user=current_user,posts=post)

@views.route('/create_post',methods=['GET','POST'])
@login_required
def  create_post():
    if request.method=="POST":
        text=request.form.get('post_text')
        if not text:
            flash('Post can not be empty',category="error")
        else:
            post=Post(post_text=text,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('post create',category="success")
    return render_template('create_post.html',user=current_user)

#for delete a post
@views.route("/delete_post/<id>")
@login_required
def delete_post(id):
    post=Post.query.filter_by(id=id).first()
    if not post:
        flash("flash does not exist",category="error")
    elif current_user.id !=post.id:
        flash("You are not right person to delete this messages",category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post Deleted",category="success")
    return redirect(url_for('views.home'))
# for specific user post to display
@views.route("/post/<username>")
@login_required
def posts(username):
    user=User.query.filter_by(username=username).first()
    if not user:
        flash("no User with that username exist .",category="error")
        return redirect(url_for('views.home'))
    posts=user.posts
    return render_template("posts.html",user=current_user,posts=posts,username=username)

#create comments
@views.route('/create_comment/<post_id>',methods=['POST'])
@login_required
def create_comment(post_id):
    cmnt=request.form.get('commnet_text')
    if not cmnt:
        flash("Null comment is not Acceptable here",category="error")
    else:
        post=Post.query.filter_by(id=post_id)
        if post:
            comment=Comments(cm_text=cmnt,author=current_user.id,post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist',category="error")
    return redirect(url_for('views.home'))

#delete commentss

@views.route("/delete_comment/<cm_id>")
@login_required
def delete_comm(cm_id):
    comm=Comments.query.filter_by(id=cm_id).first()
    if not comm:
        flash("flash does not exist",category="error")
    elif current_user.id !=comm.author and current_user.id!=comm.post.author:
        flash("You are not right person to delete this messages",category="error")
    else:
        db.session.delete(comm)
        db.session.commit()
        flash("Comment Deleted",category="success")
    return redirect(url_for('views.home'))

#like button to display the like
@views.route("/like_post/<post_id>",methods=['GET'])
@login_required
def like_post(post_id):
    post=Post.query.filter_by(id=post_id)
    like=Likes.query.filter_by(author=current_user.id,post_id=post_id).first()
    if not post:
        flash("post does not exist",category="error")
    elif like:
        print("it is working")
        db.session.delete(like)
        db.session.commit()
    else:
        like=Likes(author=current_user.id,post_id=post_id)
        db.session.add(like)
        db.session.commit()
    return redirect(url_for('views.home'))