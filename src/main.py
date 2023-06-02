import os, sys
#from icecream import ic

from utils import parse_args, read_json
from ws import last_date_sensor, compare_dates, sendValues

GLM_PATH: str | None = os.getenv(key="GLM_PATH")

TOKEN_RENEW = 0

def main() -> None:
    args = parse_args()
    credenciales:object = read_json(config=args.dbconection)
    sensor_date: str = last_date_sensor(args=credenciales, table_name=credenciales['sensor_table_name'])
    readed_date: str = last_date_sensor(args=credenciales, table_name=credenciales['procesed_table_name'])

    if (sensor_date == ""):
        sys.exit("no se encontró registro del último dato enviado")
    
    data = compare_dates(sensor_date=sensor_date, readed_date=readed_date, args=args)
    sendValues(data, args=credenciales)

if __name__ == '__main__':

    main()
