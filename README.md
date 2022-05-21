# LonnieOS

![thumbnail](%20thumbnail.png)

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

## Class structures

## Comments, Hinting and Test

```txt

pcb.py -> osPcb.py
       -> mixedPcb.py
       -> interactivePcb.py
       -> cpuBoundPcb.py

blockedQ.py  
processes.py 
os.py        
ioq.py 

main.py - > finish execute
```
<!-- https://otcatchup.util.repl.co/ -->
