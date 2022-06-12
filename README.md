# norminette for 42 schools

## Install

Requires python3.7+ (3.7, 3.8, 3.9)


### Directly inside your global commands

Install using pip
```shell
python3 -m pip install norminette
```

Upgrade pip if warnings are annoying
```shell
python3 -m pip install --upgrade pip
```

Upgrade or install the latest norminette
```shell
python3 -m pip install --upgrade norminette
```


### Inside a virtual environment

Using a virtual environment will avoid version conflicts with already globally installed packages.

```shell
python3 -m venv venv
source venv/bin/activate
pip install norminette
```

If you need to exit from a virtual environment, type `deactivate` command.

See [installing packages using pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) page for more details.


## Usage

- `norminette` - lint recursively .c/h files from the current directory;

- `norminette filename.[ch]` - lint a given .c or .h file;

- `norminette -d` - debug output (`-dd` for an extended debug report).


### Docker usage

```shell
docker build -t norminette .
docker run --rm -v $PWD:/code norminette %path%
```

You may refer to a [dockerised norminette image](https://hub.docker.com/r/alexandregv/norminette) if necessary.


## Issues reporting

If you encounter an error or an incorrect output, you can:
 - Open an issue on github (https://github.com/42School/norminette);
 - Post a message on the dedicated slack channel (#norminette-v3-beta).

Please try to include as much information as possible (the file on which it crashed and so on).


## Contribution

Feel free to do pull requests if you want to help as well.
Make sure that `run_test.sh`, run from `norminette` directory, throws no errors after your modifications.
