#FOR CI/CD Stuff
#This script finds all the .py files in the project and checks it with pylint

from pathlib import Path
import sys 

from pylint import lint  

THRESHOLD = 0  

EXIT_CODE = 0

result = list(Path(".").rglob("*.[pP][yY]"))
print(result)

for file in result:
    run = lint.Run([str(file)], do_exit=False) 


sys.exit(EXIT_CODE) 

