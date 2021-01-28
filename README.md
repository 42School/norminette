# norminette for 42 schools

## Install:

requires python3.7

```shell
pip3 install -r requirements.txt
```


To install, simply run

```shell
python3 setup.py install
```

Alternatively, you can use pip. For now it is on the testing part but will be integrated later to the main repository.
```shell
pip install -i https://test.pypi.org/simple/ norminette
```

## Usage

```
norminette
```
Runs on the current folder and any subfolder

```
norminette filename.[c/h]
```
Runs on the given filename(s)

```
norminette -d
```
Prevents stopping on various blocking errors

```
norminette -dd
```
Outputs all the debug logging

## Docker usage

```
docker build -t norminette .
cd ~/42/ft_printf
docker run -v $PWD:/code norminette /code
```

If you encounter an error or an incorrect output, you can:
 - Open an issue on github 
 - Post a message on the dedicated slack channel (#norminette-v3-beta)
    

Please try to include as much information as possible (the file on which it crashed, etc)

Feel free to do pull requests if you want to help as well. Make sure that run_test.sh properly runs after your modifications.
