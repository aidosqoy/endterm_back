import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Student
from app.forms import StudentForm
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from flask import current_app

students = Blueprint('students', __name__)


@students.route('/students')
@login_required
def list_students():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)

    students_query = Student.query.filter_by(user_id=current_user.id)

    if search:
        students_query = students_query.filter(
            (Student.first_name.ilike(f'%{search}%')) | (Student.last_name.ilike(f'%{search}%'))
        )

    students_paginated = students_query.paginate(page=page, per_page=5)
    return render_template('students/list.html', students=students_paginated, search=search)




@students.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()

    if form.validate_on_submit():
        existing_student = Student.query.filter_by(email=form.email.data).first()
        if existing_student:
            form.email.errors.append('A student with this email already exists.')
            return render_template('students/form.html', form=form)

        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            if os.path.exists(filepath):
                filename = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                os.makedirs(current_app.config['UPLOAD_FOLDER'])

            form.image.data.save(filepath)

        student = Student(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            course=form.course.data,
            email=form.email.data,
            image=filename if filename else None,
            user_id=current_user.id
        )

        db.session.add(student)
        db.session.commit()

        flash('Student added successfully.', 'success')
        return redirect(url_for('students.list_students'))

    if not form.validate_on_submit():
        print("Form validation failed:", form.errors)

    return render_template('students/form.html', form=form)

@students.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)

    if student.user_id != current_user.id and not current_user.is_admin:
        flash("You don't have permission to edit this student.", "danger")
        return redirect(url_for('students.list_students'))

    form = StudentForm(obj=student)

    if form.validate_on_submit():
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.course = form.course.data
        student.email = form.email.data

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(filepath)
            student.image = filename

        db.session.commit()
        flash('Student updated successfully', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('students/edit.html', form=form, student=student)



@students.route('/students/delete/<int:id>', methods=['POST'], endpoint='delete_student')
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)

    if student.user_id != current_user.id and not current_user.is_admin:
        flash("You don't have permission to delete this student.", "danger")
        return redirect(url_for('students.list_students'))

    db.session.delete(student)
    db.session.commit()
    flash('Student deleted.', 'info')
    return redirect(url_for('students.list_students'))






@students.route('/students/search')
def search_students():
    query = request.args.get('q')
    if query:
        results = Student.query.filter(Student.name.ilike(f"%{query}%")).all()
    else:
        results = []
    return render_template('students/search_results.html', students=results)

