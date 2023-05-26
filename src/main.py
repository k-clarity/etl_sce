import os, sys
from icecream import ic

from utils import parse_args
from ws import compara_fecha, ultimo_fecha

GLM_PATH: str | None = os.getenv(key="GLM_PATH")

TOKEN_RENEW = 0

def main() -> None:
    args = parse_args()
    fecha: str = ultimo_fecha(args=args)
    
    if (fecha == ""):
        sys.exit("no se encontró registro del último dato enviado")

    compara_fecha(fecha=fecha)

if __name__ == '__main__':

    main()
