# LonnieOS

![thumbnail](thumbnail.png)

## Run Operating System Simulator

```shell
python shell.py
```

## Project File Structure

- classes/
- tests/      (unit testing framework being used - 'unittest')
- memory.json (operating system memory overwrite)
- shell.py
- shellConfig.py
- main.py

### How the project is structured

```txt

shellConfig.py     classes/
    |               |   |
    |-------|-------|   |
            |          os.py
            |           |
          tests     shellConfig.py
            |           |
            |         main.py
            |           |
            |           |
            --------> shell.py
```


[manual](Lonnie%20Operating%20System%20Manual.pdf)
