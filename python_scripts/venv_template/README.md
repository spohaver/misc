# Virtual Environment Template
Takes a the requirements.txt file and sets up a virtual environment for it.

## How to use this:
1. add required python modules into requirements.txt
2. run `setupvenv.sh` (This will default to ~/virtual_environments unless you specify a location as an argument)
   ie. `./setupvenv.sh ~/venv`
3. Once set up, you can drop into a shell using `./venv_shell` (may need to chmod +x this)

## Requires:
* Python 3.x

## Tips:
* do a quick `pip freeze | tee requirements.txt` to build a quick one and see the output