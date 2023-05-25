import os, sys
from icecream import ic

from utils import parse_args
from ws import compara_fecha, ultimo_fecha

GLM_PATH: str | None = os.getenv(key="GLM_PATH")

TOKEN_RENEW = 0

def main() -> None:
    args = parse_args()
    fecha: str | None= ultimo_fecha(args)
    if (fecha == None):
        ic("No es posible leer la bbase de datos")
        sys.exit(__status=1)
    compara_fecha(fecha)

if __name__ == '__main__':

    main()
