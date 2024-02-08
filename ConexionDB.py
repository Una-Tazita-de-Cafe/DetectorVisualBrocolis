from sqlalchemy import create_engine,ForeignKey,func, Column,String, Integer, CHAR,Boolean,DATETIME,TIME,update,VARCHAR,Numeric,Date,DECIMAL, BINARY
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import DatosConexion

Base=declarative_base()
#Queda pendienete la implementacion de las demas tablas
class Rancho(Base):
    __tablename__="Rancho"
    idRancho=Column("idRancho", Integer,primary_key=True)
    NombreRancho=Column("NombreRancho", VARCHAR(50))
    Pais=Column("Pais",VARCHAR(30))
    Estado=Column("Estado",VARCHAR(40))
    Localidad=Column("Localidad", VARCHAR(50))
    direccion=Column("direccion", VARCHAR(50))
    Activo=Column("Activo",Boolean,default=True)
    Latitud=Column("Latitud", String)
    idCliente=Column("idCliente", Integer,ForeignKey("Cliente.idCliente"))
    def __init__(self):
        self.idRancho
        self.NombreRancho
        self.Pais
        self.Estado
        self.Localidad
        self.direccion
        self.Activo
        self.Latitud
        self.idCliente
    def __repr__(self):
        return f"{self.idRancho}, {self.NombreRancho}, {self.Pais}, {self.Estado}, {self.Localidad}, {self.direccion}, {self.Activo}, {self.Latitud} ,{self.idCliente}"
class Maquina(Base):
    __tablename__="Maquina"
    idMaquina=Column("idMaquina",Integer,primary_key=True)
    versionMaquina=Column("versionMaquina", String)
    FechaCreacion=Column("FechaCreacion", DATETIME)
    Activo=Column("Activo",Boolean,default=True)
    idRancho=Column("idRancho", Integer,ForeignKey("Rancho.idParcela"))
    def __init__(self):
       # self.idMaquina
        #self.versionMaquina
        #self.FechaCreacion
        #self.Activo
        #self.idRancho
        pass
    def __repr__(self):
        return f"{self.idMaquina}, {self.versionMaquina}, {self.FechaCreacion}, {self.Activo}, {self.idRancho}"
class Variedad(Base):
    __tablename__="Variedad"
    idVariedad=Column("idVariedad", Integer, primary_key=True)
    Nombre=Column("Nombre", VARCHAR(30))
    TiempoMaduracion=Column("TiempoMaduracion", VARCHAR(7))
    TamanoPromedio=Column("TamanoPromedio", Numeric(5,2))
    CostoPorPlantar=Column("CostoPorPlantar", Integer)
    Activo=Column("Activo",Boolean,default=True)
    def __init__(self):
        self.idVariedad
        self.Nombre
        self.TiempoMaduracion
        self.CostoPorPlantar
        self.Activo
    def __repr__(self):
        return "{self.idVariedad},{self.Nombre},{self.TiempoMaduracion},{self.CostoPorPlantar},{self.Activo}"
class Parcela(Base):
    __tablename__="Parcela"
    idParcela=Column("idParcela",Integer, primary_key=True)
    nombreParcela=Column("nombreParcela", VARCHAR(40))
    TamanoHectario=Column("TamanoHectario", Numeric(5,2))
    FechaPlantacion=Column("FechaPlantacion", Date)
    CantidadPlantada=Column("CantidadPlantada", Integer)
    SeparacionEntreBrocolis=Column("SeparacionEntreBrocolis", DECIMAL(6,2))
    DistanciaEntreSurcos=Column("DistanciaEntreSurcos", DECIMAL(6,2))
    Activo=Column("Activo",Boolean,default=True)
    idRancho=Column("idRancho", Integer,ForeignKey("Rancho.idRancho"))
    idVariedad=Column("idVariedad", Integer,ForeignKey("Variedad.idVariedad"))
    def __init__(self):
        self.idParcela
        self.nombreParcela
        self.TamanoHectario
        self.FechaPlantacion
        self.CantidadPlantada
        self.SeparacionEntreBrocolis
        self.DistanciaEntreSurcos
        self.Activo
        self.idRancho
        self.idVariedad
    def __repr__(self):
        return f"{self.idPacela}, {self.nombreParcela}, {self.TamanoParcela}, {self.FechaPlantacion}, {self.CantidadPlantada}, { self.SeparacionEntreBrocolis}, {self.DistanciaEntreSurcos}, {self.Activo}, {self.idRancho}, {self.idVariedad}"
class Cosecha(Base):
    __tablename__="Cosecha"
    idCosecha=Column("idCosecha", Integer, primary_key=True)
    Nota=Column("Nota", String)
    Activo=Column("Activo",Boolean,default=True)
    idRancho=Column("idRancho", Integer,ForeignKey("Rancho.idRancho"))
    idParcela=Column("idParcela", Integer,ForeignKey("Parcela.idParcela"))
    idMaquina=Column("idMaquina", Integer,ForeignKey("Maquina.idMaquina"))
    def __init__(self,Nota,idRancho, idParcela,idMaquina):
        self.Nota=Nota
        self.idMaquina=idMaquina
        self.idRancho=idRancho
        self.idParcela=idParcela
        
    def __repr__(self):
        return f"{self.idCosecha}, {self.Nota}, {self.idRancho}, {self.idParcela}, {self.idMaquina}"
class Estandares(Base):
    __tablename__="Estandares"
    idEstandares=Column("idEstandares", Integer, primary_key=True)
    Calibre=Column("Calibre", String)
    TamanoMaximo=Column("TamanoMaximo", Integer)
    TamanoMinimo=Column("TamanoMinimo", Integer)
    Activo=Column("Activo",Boolean,default=True)
    def __init__(self,idEstandares,Calibre,TamanoMaximo,TamanoMinimo,Activo):
        self.idEstandares=idEstandares
        self.Calibre=Calibre
        self.TamanoMaximo=TamanoMaximo
        self.TamanoMinimo=TamanoMinimo
        self.Activo=Activo
    def __repr__(self):
        return f"{self.idEstandares}, {self.Calibre}, {self.TamanoMaximo}, {self.TamanoMinimo}, {self.Activo}"
class Corte(Base):
    __tablename__="Corte"
    idCorte=Column("idCorte", Integer,primary_key=True)
    NumeroCorte=Column("NumeroCorte", Integer)
    #FechaCorte=Column("FechaCorte", DATETIME,default=func.current_date())
    #InicioCosecha=Column("InicioCosecha",TIME,func.current_time())
    FinCosecha=Column("FinCosecha",TIME)
    Activo=Column("Activo",Boolean,default=True)
    idCosecha=Column("idCosecha", Integer, ForeignKey("Cosecha.idCosecha"))
    idEstandares=Column("idEstandares", Integer,ForeignKey("Estandares.idEstandares"))
    
    def __init__(self,NumeroCorte,idCosecha,idEstandares):
        self.NumeroCorte=NumeroCorte
        self.idCosecha=idCosecha
        self.idEstandares=idEstandares
    def __repr__(self):
        return f"{self.idCorte}, {self.NumeroCorte} {self.FinCosecha}, {self.Activo}, {self.idCosecha}, {self.idEstandares}"   
class Observacion(Base):
    __tablename__="Observacion"
    idObservacion=Column("idObservacion",Integer, primary_key=True, autoincrement=True)
    CantidadObservada=Column("CantidadObservada",Integer, nullable=False)
    CantidadCortada=Column("CantidadCortada",Integer, nullable=False)
    CantidadPorEncima=Column("CantidadPorEncima",Integer, nullable=False)
    CantidadPorDebajo=Column("CantidadPorDebajo",Integer, nullable=False)
    ListaTamano=Column("ListaTamano",String)
    Activo=Column("Activo",Boolean,default=True)
    idCorte=Column(Integer,ForeignKey("Corte.idCorte"))
    def __init__(self,CantidadObservada,CantidadCortada, CantidadPorEncima,CantidadPorDebajo,ListaTamano,idCorte):
        self.CantidadObservada=CantidadObservada
        self.CantidadCortada=CantidadCortada
        self.CantidadPorEncima=CantidadPorEncima
        self.CantidadPorDebajo=CantidadPorDebajo
        self.ListaTamano=ListaTamano
        self.Activo=True
        self.idCorte=idCorte
    def __repr__(self):
        return f"({self.idObservacion}) {self.CantidadObservada} {self.CantidadCortada} {self.CantidadPorEncima} {self.CantidadPorDebajo} {self.ListaTamano} {self.Activo} {self.idCorte}"
class Prueba(Base):
    __tablename__="Prueba"
    idObservacion=Column("idObservacion",Integer, primary_key=True, autoincrement=True)
    CantidadObservada=Column("CantidadObservada",Integer, nullable=False,default=0)
    CantidadCortada=Column("CantidadCortada",Integer, nullable=False,default=0)
    CantidadPorEncima=Column("CantidadPorEncima",Integer, nullable=False,default=0)
    CantidadPorDebajo=Column("CantidadPorDebajo",Integer, nullable=False,default=0)
    Menor14=Column("Menor14", Integer,default=0)
    Cant_14=Column("Cant_14", Integer,default=0)
    Cant_15=Column("Cant_15", Integer,default=0)
    Cant_16=Column("Cant_16", Integer,default=0)
    Cant_17=Column("Cant_17", Integer,default=0)
    Cant_18=Column("Cant_18", Integer,default=0)
    Cant_19=Column("Cant_19", Integer,default=0)
    Cant_20=Column("Cant_20", Integer,default=0)
    Cant_21=Column("Cant_21", Integer,default=0)
    Cant_22=Column("Cant_22", Integer,default=0)
    Cant_23=Column("Cant_23", Integer,default=0)
    Cant_24=Column("Cant_24", Integer,default=0)
    Cant_25=Column("Cant_25", Integer,default=0)
    Cant_26=Column("Cant_26", Integer,default=0)
    Cant_27=Column("Cant_27", Integer,default=0)
    Cant_28=Column("Cant_28", Integer,default=0)
    Cant_29=Column("Cant_29", Integer,default=0)
    Cant_30=Column("Cant_30", Integer,default=0)
    Mayor30=Column("Mayor30", Integer,default=0)
    Activo=Column("Activo",Boolean,default=True)
    idCorte=Column(Integer,ForeignKey("Corte.idCorte"))
    def __init__(self,idCorte):
        self.idCorte=idCorte
    def __repr__(self):
        return f"({self.idObservacion}) {self.CantidadObservada} {self.CantidadCortada} {self.CantidadPorEncima} {self.CantidadPorDebajo} {self.Menor14} {self.Cant_14} {self.Cant_15} {self.Cant_16} {self.Cant_17} {self.Cant_18} {self.Cant_19} {self.Cant_20} {self.Cant_21} {self.Cant_22} {self.Cant_23} {self.Cant_24} {self.Cant_25} {self.Cant_26} {self.Cant_27} {self.Cant_28} {self.Cant_29} {self.Cant_30} {self.Mayor30} {self.Activo} {self.idCorte}"

    def cerrar(self):
        self.session.close()
class Creacion:
    def __init__(self,Datos):
        self.Datos=Datos
        """conexiomn sin windows autentication"""
        #engine = create_engine(f'mssql+pyodbc://{self.Datos["User"]}:{self.Datos["Pwd"]}@{self.Datos["nameServer"]}/{self.Datos["nameDB"]}?driver=ODBC+Driver+17+for+SQL+Server')
        """conexiomn con windows autentication"""
        engine = create_engine(f'mssql+pyodbc://{self.Datos["nameServer"]}/{self.Datos["nameDB"]}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes')

        Base.metadata.create_all(bind=engine)
        Session=sessionmaker(bind=engine)
        self.session=Session()
    def NuevoCorte(self,Nota, idRancho, idParcela, idMaquina,idEstandares):
       try:
           cosecha=Cosecha(Nota, idRancho, idParcela, idMaquina)
           self.session.add(cosecha)
           self.session.commit() 
           cose=self.session.query(Cosecha.idCosecha).order_by(Cosecha.idCosecha.desc()).first()
           corte=Corte(cose.idCosecha, idEstandares)
           self.session.add(corte)
           self.session.commit()
           P=self.session.query(Corte.idCorte).order_by(Corte.idCorte.desc()).first()
           observacion=Prueba(P.idCorte)
           self.session.add(observacion)
           self.session.commit()
           print("se incerto todo correctamente")
       except Exception as e:
           print("salio un error")
        
    def Incremento(self,Elemento,idE):
        try:
            R=self.session.query(getattr(Prueba,Elemento)).filter(Prueba.idObservacion==idE).scalar()
            #print(R)
            if R !=None:
                rel=update(Prueba).where(Prueba.idObservacion==idE).values({Elemento:R+1})
                self.session.execute(rel)
                self.session.commit() 
              #  R=self.session.query(getattr(Prueba,Elemento)).filter(Prueba.idObservacion==idE).scalar()
              #  print(R)
                return True
            else:
                return False
        except Exception as e:
            print("hay vamos")
            return False
        
    def prueba(self):
        """
        rel=self.session.query(Cosecha.idCosecha).order_by(Cosecha.idCosecha.desc()).first()
        P=self.session.query(Corte.idCorte).order_by(Corte.idCorte.desc()).first()
        print(rel.idCosecha)
        print(P.idCorte)
        """
        P=self.session.query(Corte.idCorte).order_by(Corte.idCorte.desc()).first()
        observacion=Prueba(P.idCorte)
        self.session.add(observacion)
        self.session.commit()
        #ref=self.session.query(Maquina).all()
        #for _ in ref:
         #   print(_)
    #session.commit()
    #dirrectorio={1:"idObservacion"}
    #R=session.query(getattr(Prueba,Elemento)).filter(Prueba.idObservacion==1).scalar()
    #rel=update(Prueba).where(Prueba.idObservacion==1).values({Elemento:session.query(getattr(Prueba,Elemento)).filter(Prueba.idObservacion==1).scalar()+1})
    #session.execute(rel)
    #session.commit()
    #R=session.query(getattr(Prueba,Elemento)).filter(Prueba.idObservacion==1).scalar()
    #print(R)

#Incremento("Cant_15", session);
Datos=DatosConexion.Datos
obj=Creacion(Datos)
print(obj.Incremento("Cant_14",1))
#obj.NuevoCorte("Prueba",1,1,1,1)
#obj.prueba()






















