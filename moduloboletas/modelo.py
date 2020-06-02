from moduloboletas import db

class Cliente(db.Model) :
    rut_cliente = db.Column(db.String(20), primary_key = True)
    nombre = db.Column(db.String(100))
    boletas = db.relationship("Boleta",backref='Cliente',lazy=True)
    def __init__(self,rut_cliente,nombre):
        self.rut_cliente = rut_cliente
        self.nombre = nombre

insumoServicio = db.Table('insumoservicio',
    db.Column('id_insumo', db.Integer, db.ForeignKey('insumo.id_insumo'),
    primary_key=True),
    db.Column('id_servicio', db.Integer,db.ForeignKey('servicio.id_servicio'),
    primary_key=True),
    db.Column('cantidad', db.Integer),
)

boletaServicio = db.Table('boletaServicio',
    db.Column('id_boleta', db.Integer, db.ForeignKey('boleta.id_boleta')),
    db.Column('id_servicio', db.Integer, db.ForeignKey('servicio.id_servicio'))
)

class Insumo(db.Model) :
    id_insumo = db.Column(db.Integer,  primary_key = True)
    nombre_insumo = db.Column(db.String(100))
    valor = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    def __init__(self,id_insumo,nombre_insumo,valor,stock):
        self.id_insumo = id_insumo
        self.nombre_insumo = nombre_insumo
        self.valor = valor
        self.stock = stock

@dataclass
class Servicio (db.Model):
    __tablename__ = 'servicio'
    id_servicio = db.Column(db.Integer, primary_key = True, nullable=False)
    nombre_servicio = db.Column(db.String(100))
    insumoServicio = db.relationship('Insumo', secondary=insumoServicio,
        lazy='subquery', backref=db.backref('pages',lazy=True))
    def __init__(self, id_servicio, nombre_servicio,insumos):
        self.id_servicio = id_servicio
        self.nombre_servicio = nombre_servicio
        self.insumos= insumos

class Boleta(db.Model) :
    __tablename__ = 'boleta'
    id_boleta = db.Column(db.Integer, primary_key = True)
    rut_cliente = db.Column(db.String(20), db.ForeignKey(
    'cliente.rut_cliente'),nullable=False)
    boletaServicio = db.relationship("Servicio",
                               secondary=boletaServicio)
    valor = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)
    nula =  db.Column(db.Boolean, default=False)

    def __init__(self,rut_cliente, valor, fecha):
        #self.id_boleta = id_boleta
        self.rut_cliente = rut_cliente
        self.fecha = fecha
        self.valor = valor

class Reporte(db.Model):
    id_reporte = db.Column(db.Integer, primary_key=True)
    mayor_servicio = db.Column(db.Integer, db.ForeignKey(
    'servicio.id_servicio'),nullable=False)
    mayor_insumo = db.Column(db.Integer, db.ForeignKey(
    'insumo.id_insumo'),nullable=False)
    monto_total = db.Column(db.Integer)
    cantidad_boletas = db.Column(db.Integer)
    dia = db.Column(db.Integer)
    mes = db.Column(db.Integer)
    anio = db.Column(db.Integer)

    def __init__(self,mes,anio):
        self.mes = mes
        self.anio = anio
        cantidad_boletas=0
        monto_total=0
        boletas = db.session.query(Boleta).filter(
        extract('year', Boleta.fecha)==anio).filter(
        extract('month', Boleta.fecha)==mes).all()
        for boleta in boletas:
            cantidad_boletas+=1
            print(monto_total)
            monto_total += boleta.valor
            servicios = boleta.boletaServicio
            for servicio in servicios:
                self.mayor_servicio = servicio
                for insumo in servicio.insumoServicio:
                    self.mayor_insumo = insumo

        self.cantidad_boletas=cantidad_boletas
        self.monto_total= monto_total
