import json, argparse, psycopg2, os

def read_json(config) -> object:
    with open(file=config) as archivo_credenciales:
        credenciales: object = json.load(archivo_credenciales)
    return credenciales

def read_files(file):
    with open(os.path.join("./fecha_ult.json"), 'w') as file:
            dt = json.dump(data, file)
            return dt
def parse_args():
    parser = argparse.ArgumentParser(description="SCE running file")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('--db-connection', dest="dbconection", help="path to configuration file", required=True)
    args = parser.parse_args()
    return args

def connection(credenciales):
    try:
        conexion = psycopg2.connect(    host=credenciales["host"],
                                                    database=credenciales["dbname"],
                                                    user=credenciales["user"],
                                                    password=credenciales["password"])
    except psycopg2.Error as e:
        print("Ocurrió un error al conectar a PostgreSQL: ", e)
    return conexion