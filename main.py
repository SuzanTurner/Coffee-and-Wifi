from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired(message="Enter a Cafe Name")])
    location = StringField('Location', validators=[DataRequired(message="Enter its Location")])
    rating = StringField('Rating', validators=[DataRequired(message="Enter its Rating")])
    check_box_wifi = BooleanField('WiFi Available')
    check_box_charge = BooleanField('Charging Points Available')
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        f = r"static/database.txt"
        with open(f, mode='a', newline='') as file:
            # Extract form data
            n = form.name.data
            l = form.location.data
            r = form.rating.data
            wifi = "True" if form.check_box_wifi.data else "False"
            charge = "True" if form.check_box_charge.data else "False"

            # Write to the file
            file.write(f"{n},{l},{r},{wifi},{charge}\n")
        return redirect('/cafes')

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    cafes_data = []
    with open(r'static/database.txt', mode='r') as file:
        lines = file.readlines()
    for line in lines:
        cafes_data.append(line.strip().split(','))

    return render_template('cafes.html', cafes=cafes_data)


if __name__ == '__main__':
    app.run(debug=True)
