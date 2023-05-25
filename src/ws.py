import psycopg2,datetime,json,os
from icecream import ic
from utils import read_json, connection

def ultimo_fecha(args):
    credenciales:object = read_json(config=args.dbconection)
    try:
        conexion = connection(credenciales)
    except:
        ic ("No hay conexión con ola base de datos")
    try:
        curFecha = conexion.cursor()
        sqlFecha: str = f"SELECT MAX(fecha) FROM {credenciales['table_name']}"
        curFecha.execute(query=sqlFecha,vars=())
        conexion.commit()
        datosFecha: list[tuple[json, ...]] = curFecha.fetchall()
        for row in datosFecha:
                fecha = row[0]
        fecha = str(object=fecha)
        curFecha.close()
        return fecha
    except Exception as e:
        print('Error al encontrar la ultima fecha: '+str(e))
         
def sendValues(inf):
     
     print(inf)
    # headers={ 'content-type': "application/json",
    #           'cache-control': "no-cache"
    #     }
    # method="POST"
    # try:
    #     ssl._create_default_https_context=ssl._create_unverified_context
    #     data=json.dumps(inf)
    #     connection = http.client.HTTPSConnection("data.keraunos.co",timeout=10.0)
    #     connection.request(method,"/SCEKER/",body=data,headers=headers)
    #     response = connection.getresponse()
    #     return response.status
    # except Exception as e:
    #     fechaIngFallo = datetime.datetime.now() - datetime.timedelta(hours = 5)
    #     dataFallo = str(e)
    #     sqlInsFallo = 'INSERT INTO fallos(fallo,script,fecha) VALUES (%s,%s,%s)'
    #     cursorFallo = conexion.cursor()
    #     cursorFallo.execute(sqlInsFallo, (dataFallo,'EnvioWS',fechaIngFallo))
    #     conexion.commit()
    #     cursorFallo.close()
    # finally:
    #     connection.close()
def compara_fecha(fecha):
   try:
      
      isempty = os.stat('./fecha_ult.json').st_size == 0
      print ("Compara: "+str(isempty))
      if isempty == True:
        data = {}
        data['fecha'] = fecha      
        with open(os.path.join("./fecha_ult.json"), 'w') as file:
            json.dump(data, file)
        file.close()
      else:
        dataEnv = []
        with open(os.path.join("./fecha_ult.json"), 'r') as d:
            dt = json.load(d)
        fechaC = str(dt[ "fecha" ])
        if fecha == fechaC:
            print ("")
        else:
            data = {}
            data['fecha'] = fecha      
            with open(os.path.join("./fecha_ult.json"), 'w') as file:
                json.dump(data, file)
            curMCE = conexion.cursor()
            sqlMCE = "SELECT fecha,maximo,ce from electric_field_mean where fecha > %s"
            curMCE.execute(sqlMCE,(fechaC,))
            conexion.commit()
            datosMCE = curMCE.fetchall()
            for row in datosMCE:
                d = '0'
                dataEnv.append({"fecha":str(row[0]),"ce":str(row[2]),"dce":str(d)})
                body={"solicitud":"sce","id":"Santo Tomas","data":dataEnv}
            #response = requests.post('https://data.keraunos.co/SCEKER/', data = body)
            response=sendValues(body)
            file.close()
            curMCE.close()     
   except Exception as e:
     print('Error compara: '+str(e))
     fechaIngFallo = datetime.datetime.now() - datetime.timedelta(hours = 5)
     dataFallo = str(e)
     sqlInsFallo = 'INSERT INTO fallos(fallo,script,fecha) VALUES (%s,%s,%s)'
    #  cursorFallo = conexion.cursor()
    #  cursorFallo.execute(sqlInsFallo, (dataFallo,'Compara_Fecha',fechaIngFallo))
    #  conexion.commit()
    #  cursorFallo.close()


