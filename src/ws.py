from ast import arg
import datetime, json, os, sys
#from icecream import ic
from numpy import arange
from utils import read_json, connection
import numpy as np

def last_date_sensor(args:object, table_name) -> str:
    
    
    try:
        conexion = connection(args)
    except:
        
        print ("No hay conexión con ola base de datos")
    try:
        curFecha = conexion.cursor()
        sqlFecha: str = f"SELECT MAX(fecha) FROM {args['sensor_table_name']}"
        curFecha.execute(query=sqlFecha,vars=())
        conexion.commit()
        fecha: str = curFecha.fetchall()[0][0]
        curFecha.close()
        print (fecha)
        return fecha
    except Exception as e:
        print('Error al encontrar la ultima fecha: '+str(e))
        return ""
         
def sendValues(inf, args:object):
     
     print(inf)
     
     try:
        conexion = connection(args)
     except:
        ic ("No hay conexión con ola base de datos")
     last_date = inf[-1][0]
     last_date.strftime("%Y/%m/%d %H:%M:%S")
     print (last_date)
     curDateLast = conexion.cursor()
     sqlFecha: str = "INSERT INTO "+args['procesed_table_name']+" (date) VALUES (%s);" 
     print (f"{sqlFecha}{last_date}")
     curDateLast.execute(sqlFecha, (last_date,))
     conexion.commit()
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

def compare_dates(sensor_date:str, readed_date:str, args:object):
    if (sensor_date != readed_date):
        credenciales:object = read_json(config=args.dbconection)
        try:
            conexion = connection(credenciales)
        except:
            ic("no se pudo establecer conexión con la base de datos")
        try:
            
            sensor_date = np.datetime64(sensor_date)
            readed_date = np.datetime64(readed_date)
        
            curMCE = conexion.cursor()
            sqlMCE = "SELECT fecha,maximo,ce from electric_field_mean where fecha > %s"
            if (sensor_date < readed_date):
                curMCE.execute(sqlMCE,(str(sensor_date),))
            else:
                curMCE.execute(sqlMCE,(str(readed_date),))
            conexion.commit()
            datosMCE = curMCE.fetchall()
            curMCE.close()
            return datosMCE     
        except Exception as e:
            print('Error compara: '+str(e))
            fechaIngFallo = datetime.datetime.now() - datetime.timedelta(hours = 5)
            dataFallo = str(e)
            sqlInsFallo = 'INSERT INTO fallos(fallo,script,fecha) VALUES (%s,%s,%s)'
            #  cursorFallo = conexion.cursor()
            #  cursorFallo.execute(sqlInsFallo, (dataFallo,'Compara_Fecha',fechaIngFallo))
            #  conexion.commit()
            #  cursorFallo.close()
      
      


