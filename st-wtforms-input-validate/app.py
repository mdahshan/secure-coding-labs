from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import InputRequired, Length, Email, Regexp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        InputRequired(),
        Length(max=50),
        Regexp('^[A-Za-z ]+$', 
               message="Full name can only contain letters and spaces.")])
    
    date_of_birth = DateField('Date of Birth', 
                              format='%Y-%m-%d', validators=[InputRequired()])
    
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # If form is valid, show a success message with user details
        flash(f'''Registration Successful!
              Full Name: {form.full_name.data}
              Date of Birth: {form.date_of_birth.data.strftime("%d/%m/%Y")}
              Email: {form.email.data}
              Password: {"*" * len(form.password.data)}''', 'success')
        return redirect(url_for('register'))
    elif form.errors:
        # Display form errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field.replace("_", " ").capitalize()}: {error}', 'error')
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
