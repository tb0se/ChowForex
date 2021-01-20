# Import flask dependencies
from flask import render_template, Blueprint, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user

from app import db
from app.forms import PostForm
from app.models import Post, User
from app.utils.decorators import check_confirmed

blog = Blueprint('blog', __name__, url_prefix="/blog", static_folder ='static', template_folder='templates')

# Blog home(show all posts)
# TODO: Show a summary of the post content
@blog.route('/')
def home():

    # Paginate the posts
    page_no = request.args.get('page',1,type=int)
    # posts = Post.query.paginate(page=page_no,per_page=5)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page_no,per_page=5)
    return render_template("blog/index.html",posts=posts)


# Create a new post
@blog.route('/post/new',methods=['POST','GET'])
@login_required
@check_confirmed
def new_post():
    post_form = PostForm()
    if request.method == 'POST' and post_form.validate_on_submit():

        # Get form data
        title = post_form.title.data
        content = post_form.content.data

        # Create Post
        post = Post(title=title,content=content,author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Your post has been created','success')
        return redirect(url_for('blog.home'))
    return render_template("blog/create_post.html", form=post_form, title="New Post",legend="New Post")


# View post
# TODO: Change the way we view the post https://getbootstrap.com/docs/4.5/examples/blog/
@blog.route('/post/<int:post_id>')
def post(post_id):
    # post = Post.query.get(post_id)
    post = Post.query.get_or_404(post_id)
    return render_template("blog/view_post.html",title=post.title,post=post)


# Update a post
@blog.route('/post/<int:post_id>/update',methods=['POST','GET'])
@login_required
@check_confirmed
def update_post(post_id):

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    post_form = PostForm()
    if request.method == 'POST' and post_form.validate_on_submit():
        post.title = post_form.title.data
        post.content = post_form.content.data
        db.session.commit()
        flash('Post successefully updated', 'success')
        return redirect(url_for('blog.post',post_id=post.id))

    elif request.method == 'GET':   
        post_form.title.data = post.title
        post_form.content.data = post.content
    
    return render_template("blog/create_post.html", form=post_form, title="Update Post",legend="Update post") 

@blog.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
@check_confirmed
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post successfully delete', 'success')
    return redirect(url_for('blog.home'))

# Show all posts for this specific user
@blog.route('/user/<string:email>')
def user_posts(email):
    page_no = request.args.get('page',1,type=int)
    user = User.query.filter_by(email=email).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page_no,per_page=5)
    return render_template("blog/user_posts.html",posts=posts, user=user)