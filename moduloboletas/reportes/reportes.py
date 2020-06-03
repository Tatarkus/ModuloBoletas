from flask import Flask, url_for, render_template, redirect, request, Blueprint
import datetime
from moduloboletas.modelo import Reporte
reportes_bp = Blueprint('reportes', __name__, template_folder='templates')

@reportes_bp.route('/obtenerReporte',methods=['POST'])
def obtenerReporte():
    anio= int(request.form['year'])
    mes= int(request.form['month'])
    miReporte = Reporte(mes,anio)
    miMes = datetime.date(anio, mes, 1).strftime('%B')
    print(miMes)
    return render_template("reporte.html",reporte = miReporte, mes=miMes, anio = anio)
