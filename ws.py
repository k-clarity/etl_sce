import psycopg2,datetime,json,os,requests,ssl,http.client,time
from bd import conexion
try:
 def ultimo_fecha():
   try:
      curFecha = conexion.cursor()
      sqlFecha = "SELECT MAX(fecha) FROM electric_field_mean";
      curFecha.execute(sqlFecha,())
      conexion.commit()
      datosFecha = curFecha.fetchall()
      for row in datosFecha:
            fecha = row[0];
      fecha = str(fecha)
      curFecha.close()
      return fecha
   except Exception as e:
     print('Error: '+str(e))
     fechaIngFallo = datetime.datetime.now() - datetime.timedelta(hours = 5)
     dataFallo = str(e)
     sqlInsFallo = 'INSERT INTO fallos(fallo,script,fecha) VALUES (%s,%s,%s)';
     cursorFallo = conexion.cursor()
     cursorFallo.execute(sqlInsFallo, (dataFallo,'Ultimo_fecha',fechaIngFallo))
     conexion.commit()
     cursorFallo.close()      
 def sendValues(inf):
    headers={ 'content-type': "application/json",
              'cache-control': "no-cache"
        }
    method="POST"
    try:
        ssl._create_default_https_context=ssl._create_unverified_context
        data=json.dumps(inf)
        connection = http.client.HTTPSConnection("data.keraunos.co",timeout=10.0)
        connection.request(method,"/SCEKER/",body=data,headers=headers)
        response = connection.getresponse()
        return response.status
    except Exception as e:
        fechaIngFallo = datetime.datetime.now() - datetime.timedelta(hours = 5)
        dataFallo = str(e)
        sqlInsFallo = 'INSERT INTO fallos(fallo,script,fecha) VALUES (%s,%s,%s)';
        cursorFallo = conexion.cursor()
        cursorFallo.execute(sqlInsFallo, (dataFallo,'EnvioWS',fechaIngFallo))
        conexion.commit()
        cursorFallo.close()
    finally:
        connection.close()
 def compara_fecha(fecha):
   try:
      dir = 'C:\scripts\sce'
      file_name = "fecha_ult.json"
      isempty = os.stat('C:/scripts/sce/fecha_ult.json').st_size == 0
      print (isempty)
      if isempty == True:
        data = {}
        data['fecha'] = fecha      
        with open(os.path.join(dir, file_name), 'w') as file:
            json.dump(data, file)
        file.close()
      else:
        dataEnv = []
        dir = 'C:\scripts\sce'
        file_name = "fecha_ult.json"
        with open(os.path.join(dir, file_name), 'r') as d:
            dt = json.load(d)
        fechaC = str(dt[ "fecha" ])
        if fecha == fechaC:
            print ("")
        else:
            data = {}
            data['fecha'] = fecha      
            with open(os.path.join(dir, file_name), 'w') as file:
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
     sqlInsFallo = 'INSERT INTO fallos(fallo,script,fecha) VALUES (%s,%s,%s)';
     cursorFallo = conexion.cursor()
     cursorFallo.execute(sqlInsFallo, (dataFallo,'Compara_Fecha',fechaIngFallo))
     conexion.commit()
     cursorFallo.close()


 fecha= ultimo_fecha()
 compara_fecha(fecha)
    

except Exception as e:
    print('Error: '+str(e))
    fechaIngError = datetime.datetime.now() - datetime.timedelta(hours = 5)
    sqlInsError = 'INSERT INTO fallos(fallo,script,fecha) VALUES (%s,%s,%s)';
    cursorError = conexion.cursor()
    cursorError.execute(sqlInsError, (str(e),'WS',fechaIngError))
    conexion.commit()
    cursorError.close()
    conexion.close()
