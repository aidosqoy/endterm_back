from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app.forms import EditUserForm
from app.models import User
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)

    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')

    query = User.query
    if search_query:
        query = query.filter(
            (User.name.ilike(f'%{search_query}%')) |
            (User.email.ilike(f'%{search_query}%'))
        )

    users = query.order_by(User.id).paginate(page=page, per_page=5)

    return render_template('admin/dashboard.html', users=users, search_query=search_query)

@admin_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not getattr(current_user, 'is_admin', False):
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)
    form = EditUserForm(original_email=user.email, obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        db.session.commit()
        flash('User Updated', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/edit_user.html', form=form)


@admin_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You can't delete yourself.", 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.name} deleted', 'success')
    return redirect(url_for('admin.admin_dashboard'))

