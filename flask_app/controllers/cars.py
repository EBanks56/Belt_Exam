from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car

@app.route('/new/car')
def newCar():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('create.html', user=User.get_one(data))

@app.route('/create/car', methods = ['POST'])
def createPost():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_series(request.form):
        return redirect('/new/car')
    data = {
        'price': request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Car.save(data)
    return redirect('/home')

@app.route('/edit/<int:id>')
def edit_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit.html", car=Car.get_one_with_user(data), user=User.get_one(user_data))

@app.route('/update', methods=['POST'])
def update_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_series(request.form):
        return redirect('/new/car')
    data = {
        'price': request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description'],
        'id': request.form['id']
    }
    Car.update(data)
    return redirect('/home')

@app.route('/view/<int:id>')
def show_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    return render_template("view.html", car=Car.get_one_with_user(data))

@app.route('/delete/<int:id>')
def delete_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Car.delete(data)
    return redirect('/home')
