from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Car:
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creatorFirst = data['creatorFirst']
        self.creatorLast = data['creatorLast']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO cars (price, model, make, year, description, created_at, updated_at, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL('car_dealz').query_db(query, data)

    @classmethod
    def get_all_cars(cls):
        query = "SELECT users.first_name as creatorFirst, users.last_name as creatorLast, cars.* FROM users JOIN cars ON users.id = cars.user_id;"
        results = connectToMySQL('car_dealz').query_db(query)
        all_cars = []
        for row in results:
            all_cars.insert(0, cls(row))
        return all_cars

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT users.first_name as creatorFirst, users.last_name as creatorLast, cars.* FROM users JOIN cars ON users.id = cars.user_id WHERE cars.id = %(id)s;"
        results = connectToMySQL('car_dealz').query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET price=%(price)s, model=%(model)s, year=%(year)s, description=%(description)s, updated_at=NOW() WHERE id=%(id)s"
        return connectToMySQL('car_dealz').query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars WHERE id=%(id)s"
        return connectToMySQL('car_dealz').query_db(query,data)

    @staticmethod
    def validate_series(car):
        is_valid = True
        if car['price'] == '' or int(car['price']) < 1:
            flash("'Car Price' must be over $0.")
            is_valid = False
        if len(car['model']) < 1:
            flash("'Car Model' field is required.")
            is_valid = False
        if len(car['make']) < 1:
            flash("'Car Make' field is required.")
            is_valid = False
        if car['year'] == '' or int(car['year']) < 1900:
            flash("'Car Year' not valid.")
            is_valid = False
        if len(car['description']) < 1:
            flash("'Car Description' field is required.")
            is_valid = False
        return is_valid

