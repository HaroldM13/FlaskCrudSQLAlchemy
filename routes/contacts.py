from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.contact import Contact
from utils.db import db


contacts = Blueprint('contacts', __name__)

#HOME
@contacts.route('/')
def index():
    #users = db.session.execute(db.select(Contact).order_by(Contact.id)).scalars()
    users = Contact.query.all()
    return render_template("index.html", users=users)


#ADD CONTACT
@contacts.route('/new', methods=['POST'])
def add_contact():
    fullname = request.form['fullname']
    email = request.form['email']
    phone = request.form['phone']

    new_contact = Contact(fullname,email,phone)

    db.session.add(new_contact)
    db.session.commit()

    flash("Contact added successfully!!!")

    return redirect(url_for('contacts.index'))

#UPDATE CONTACT
@contacts.route('/update/<id>', methods=['GET','POST'])
def update(id):
    user = db.get_or_404(Contact, id)

    if request.method == 'POST':
        user.fullname = request.form['fullname']
        user.email = request.form['email']
        user.phone = request.form['phone']

        db.session.commit()

        flash("Contact Updated Successfully!!!")

        return redirect(url_for("contacts.index"))
    
    #user = db.session.execute(db.select(Contact).where(Contact.id == id)).scalar_one()
    return render_template('update.html', user = user)


#DELETE CONTACT
@contacts.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    contact = db.get_or_404(Contact, id)

    db.session.delete(contact)
    db.session.commit()

    flash("Contact Deleted Successfully!!!")

    return redirect(url_for('contacts.index'))

#ABOUT
@contacts.route('/about')
def about():
    return render_template('about.html')