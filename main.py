import os, sys
from ws import ultimo_fecha
from ws import compara_fecha

GLM_PATH = os.getenv("GLM_PATH")

TOKEN_RENEW = 0

def main():
    fecha= ultimo_fecha()
    compara_fecha(fecha)

if __name__ == '__main__':

    main()
