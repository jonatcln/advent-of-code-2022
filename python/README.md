# Python

## Dependencies

For nicely highlighted and formatted tracebacks, you can optionally install
[Rich](https://github.com/Textualize/rich):

```sh
pip3 install rich
```

## How to run?

Put your input files in a folder `input/` using the naming pattern `dayXX.txt`.
Note that `XX`, the day number, should contain a leading zero if necessary.

Make sure the `main.py` file is executable:

```sh
chmod +x main.py
```

Then, to run day `X` and part `Y`, use:

```sh
./main.py -d X -p Y
```

For other options (such as specifying a different input file, or automatically
using today's day), run the script with the `--help` flag.

```console
$ ./main.py --help
usage: main.py [-h] [-d DAY] [-p PART] [-i INPUT_STRING | -f INPUT_FILE]

optional arguments:
  -h, --help       show this help message and exit
  -d DAY           day to run (default: today's day)
  -p PART          part to run (default: last implemented)
  -i INPUT_STRING  input string
  -f INPUT_FILE    input filename (default: `input/dayXX.txt`)
```
