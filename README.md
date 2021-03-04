# norminette for 42 schools

## Install:

requires python3.7+ (3.7, 3.8, 3.9)

Install using pip.
```shell
pip install norminette
```
To upgrade an existing install, use
```shell
pip install --upgrade norminette
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
