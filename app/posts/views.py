from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
)

from app import db
from app.posts import posts_bp
from app.posts.models import Post, Tag
from app.forms import PostForm


@posts_bp.route("/")
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("posts/list.html", posts=posts)


@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.body.data,
            user_id=form.author_id.data,
        )

        selected_tag_ids = form.tags.data
        if selected_tag_ids:
            tags = Tag.query.filter(Tag.id.in_(selected_tag_ids)).all()
            post.tags.extend(tags)

        db.session.add(post)
        db.session.commit()
        flash("Post created.", "success")
        return redirect(url_for("posts.list_posts"))

    return render_template("posts/create.html", form=form)


@posts_bp.route("/<int:post_id>")
def post_detail(post_id: int):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/detail.html", post=post)

