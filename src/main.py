import os, sys
from icecream import ic

from utils import parse_args
from ws import last_procesed_date, last_date_sensor, compare_dates

GLM_PATH: str | None = os.getenv(key="GLM_PATH")

TOKEN_RENEW = 0

def main() -> None:
    args = parse_args()
    sensor_date: str = last_date_sensor(args=args)
    readed_date: str = last_procesed_date(args=args)

    if (fecha_sensor == ""):
        sys.exit("no se encontró registro del último dato enviado")
    
    compare_dates(sensor_date=sensor_date, readed_date=readed_date, args=args)

if __name__ == '__main__':

    main()
