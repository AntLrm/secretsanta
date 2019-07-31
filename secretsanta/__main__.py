import sys

from secretsanta.app import app

if __name__ == "__main__" :
    secretsanta = app()
    secretsanta.run(sys.argv[1:])
