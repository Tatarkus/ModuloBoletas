from flask import Flask, url_for, render_template, redirect, request, Blueprint, flash
from flask import jsonify
from moduloboletas.modelo import Cliente, Boleta, Servicio
from moduloboletas import db
from datetime import date
boletas_bp = Blueprint('boletas', __name__, template_folder='templates')

@boletas_bp.route('/')
def index():
    misBoletas = Boleta.query.all()
    misServicios = Servicio.query.all()
    serviciosJson= jsonify(misServicios)
    return render_template("index.html", boletas=misBoletas,
    servicios=misServicios)

@boletas_bp.route('/nuevaBoleta',methods=['POST'])
def nuevaBoleta():
    if request.method=='POST':
        cliente= request.form['cliente']
        valor = request.form['valor']
        fecha = date.today()

        if Cliente.query.get(cliente) == None:
            flash("ERROR: Cliente no encontrado",'error')
            return redirect(url_for('index'))
        idservicio = request.form.get('servicios_dropdown')
        servicio = Servicio.query.get(idservicio)
        boleta=Boleta(cliente, valor,fecha)
        boleta.boletaServicio.append(servicio)
        db.session.add(boleta)
        db.session.commit()
        flash("Boleta Agregada Correctamente")
    return redirect(url_for('boletas.index'))

@boletas_bp.route('/buscar',methods=['POST'])
def buscarBoleta():
    if request.method=='POST':
        id= request.form['buscar']
        boleta = Boleta.query.filter_by(id_boleta = id)
        return render_template("index.html", boletas =boleta)

@boletas_bp.route('/anular:/<int:id_boleta>',methods=['GET','POST'])
def anularBoleta(id_boleta):
    id= id_boleta
    print("Anulando boleta...")
    boleta = db.session.query(Boleta).filter_by(id_boleta=id).first()
    boleta.nula = True
    db.session.commit()
    return redirect(url_for('boletas.index'))
