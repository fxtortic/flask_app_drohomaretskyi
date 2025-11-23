from flask import render_template, redirect, url_for, flash, request

from app import db
from app.posts import posts_bp
from app.posts.models import Post
from app.forms import PostForm


@posts_bp.route("/", methods=["GET"])
def index():
    posts = (
        Post.query.order_by(Post.posted.desc())
        .filter_by(is_active=True)
        .all()
    )
    return render_template("index.html", posts=posts)


@posts_bp.route("/<int:post_id>", methods=["GET"])
def detail(post_id: int):
    post = Post.query.get_or_404(post_id)
    return render_template("detail.html", post=post)


@posts_bp.route("/create", methods=["GET", "POST"])
def create():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            author=form.author.data or "Anonymous",
        )
        db.session.add(post)
        db.session.commit()

        flash("Пост успішно створено!", "success")
        return redirect(url_for("posts.index"))

    if request.method == "POST" and not form.validate():
        flash("Перевірте правильність заповнення форми.", "error")

    return render_template("create.html", form=form)
