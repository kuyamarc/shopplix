import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "listdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

heroku = Heroku(app)

db = SQLAlchemy(app)

class List(db.Model):
	title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

	def __repr__(self):
		return "<Title: {}>".format(self.title)

@app.route("/", methods=["GET", "POST"])
def home():
	if request.form:
		try:
			list = List(title=request.form.get("title"))
			db.session.add(list)
			db.session.commit()
		except Exception as e:
			print("Failed to add list")
			print(e)
	lists = List.query.all()
	return render_template("index.html", lists=lists)

@app.route("/update", methods=["POST"])
def update():
	try:
		newtitle = request.form.get("newtitle")
		oldtitle = request.form.get("oldtitle")
		list = List.query.filter_by(title=oldtitle).first()
		list.title = newtitle
		db.session.commit()
	except Exception as e:
			print("Failed to add list")
			print(e)	
	return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
	title = request.form.get("title")
	list = List.query.filter_by(title=title).first()
	db.session.delete(list)
	db.session.commit()
	return redirect("/")

if __name__ == ' __main__':
	#app.debug = True
	app.run()