from flask import render_template, redirect, url_for, request
from application.models import characters, classes
from application import app, db
from application.forms import NewForm, EditForm, DeleteForm
from sqlalchemy.orm import join
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

@app.route("/")
@app.route("/home")
def home():
    Characters = characters.query.all()
    return render_template("home.html", title="Home", Characters=Characters)

@app.route('/new', methods=["GET", "POST"])
def new():
    form = NewForm()
    if form.validate_on_submit():
        new = characters(name=form.name.data,clas=form.clas.data,race=form.race.data,level=form.level.data,CON=form.CON.data,DEX=form.DEX.data,STR=form.STR.data,INT=form.INT.data,WIS=form.WIS.data,CHA=form.CHA.data,Health=form.Health.data,Armor=form.Armor.data,Spell_points=form.Spell_points.data,Speed=form.Speed.data)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print(form.errors)

    return render_template("new.html", title="New", form=form)

@app.route("/delete/<identity>", methods=["GET", "POST"])
def delete(identity):
    form = DeleteForm()
    if form.validate_on_submit():
        char = characters.query.filter_by(id=identity).first()
        db.session.delete(char)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("delete.html", form=form, identity=identity, title="Delete")

@app.route("/deleted/<identity>", methods=["GET", "POST"])
def deleted(identity):
    form = DeleteForm()
    char = characters.query.filter_by(id=identity).first()
    db.session.delete(char)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/sheet/<identity>', methods=["GET", "POST"])
def sheet(identity):
    sql_cmd = text("select * from characters inner join classes where characters.clas = classes.clas and characters.id = {};".format(identity))
    data = db.engine.execute(sql_cmd).fetchall()
    form = DeleteForm()
    if form.validate_on_submit():
        char = characters.query.filter_by(id=identity).first()
        db.session.delete(char)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('sheet.html', title='Sheet',identity=identity, data=data, classes=classes, form=form)

@app.route("/edit/<identity>", methods=["GET", "POST"])
def edit(identity):
    form = EditForm()
    if form.validate_on_submit():
        characters.query.filter_by(id=identity).first().name = form.name.data
        characters.query.filter_by(id=identity).first().race = form.race.data
        characters.query.filter_by(id=identity).first().clas = form.clas.data
        characters.query.filter_by(id=identity).first().level = form.level.data
        characters.query.filter_by(id=identity).first().CON = form.CON.data
        characters.query.filter_by(id=identity).first().DEX = form.DEX.data
        characters.query.filter_by(id=identity).first().STR = form.STR.data
        characters.query.filter_by(id=identity).first().INT = form.INT.data
        characters.query.filter_by(id=identity).first().WIS = form.WIS.data
        characters.query.filter_by(id=identity).first().CHA = form.CHA.data
        characters.query.filter_by(id=identity).first().Health = form.Health.data
        characters.query.filter_by(id=identity).first().Armor = form.Armor.data
        characters.query.filter_by(id=identity).first().Spell_points = form.Spell_points.data
        characters.query.filter_by(id=identity).first().Speed = form.Speed.data
        db.session.commit()
        return redirect(url_for('sheet', identity=identity))
    elif request.method == 'GET':
        form.name.data = characters.query.filter_by(id=identity).first().name
        form.race.data = characters.query.filter_by(id=identity).first().race
        form.clas.data = characters.query.filter_by(id=identity).first().clas
        form.level.data = characters.query.filter_by(id=identity).first().level
        form.CON.data = characters.query.filter_by(id=identity).first().CON
        form.DEX.data = characters.query.filter_by(id=identity).first().DEX
        form.STR.data = characters.query.filter_by(id=identity).first().STR
        form.INT.data = characters.query.filter_by(id=identity).first().INT
        form.WIS.data = characters.query.filter_by(id=identity).first().WIS
        form.CHA.data = characters.query.filter_by(id=identity).first().CHA
        form.Health.data = characters.query.filter_by(id=identity).first().Health
        form.Armor.data = characters.query.filter_by(id=identity).first().Armor
        form.Spell_points.data = characters.query.filter_by(id=identity).first().Spell_points
        form.Speed.data = characters.query.filter_by(id=identity).first().Speed       
    return render_template('edit.html', title='Edit', form=form)

