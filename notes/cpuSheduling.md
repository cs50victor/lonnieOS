
# CPU Virtualization

## How your computer decides on what to work on

Modern Operating Systems schedule their task on different time scales

1. Long-term scheduler
2. Mid-term Scheduler
3. Short-term Scheduler

Our machine has a bunch of threads or processes
*Process States*

- Created
- Active
- Waiting [not at the front of the ready queue]
- Ready [front of the ready queue]
- Exited

Process Task
Each process is using the CPU, or waiting for requests for some other place (like network requests, user I/O inputs)

- CPU-bound ()
- IO-bound ()