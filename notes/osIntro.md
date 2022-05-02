# Operating System Quick Intro

## Background

All this 'magic' is accomplished by genius electrical hardware architecture primarily based on the our understanding and use of electricity to represent information and perform calculations.
All programs are compiled to a version of assembly language for their specific computer architecture + OS + assembler, and finally it is assembled to machine code - 1's and 0's.

The Operating System is like the parent of all other programs you run on your computer. Manages the hardware and running programs.
Basic functions:

- load and manage processes (an abstraction for everything you run on a computer), and allow them to share the same hardware resources simultaneously
- provide interfaces to hardware via system calls
- provide a filesystem (an easy abstraction over the computer's storage devices)
- provide a basic user interface (for regular people to communicate with their computer)
- provide API's like device driver's that allow the other devices to communicate with out device.

Note - the operating system, threads and processes all run on the cores of the computer.
However the OS and a process cannot run at the same time as a process.

## UNIX and OS functionality separation

1. Kernel (core functionality of the os)
   - handles things like memory management, multitasking and I/O
2. Programs and Libraries

## Brief History

Computers in the 40's and early 50's could only run one process at a time
Running computer took hours/weeks because humans had to manually operate computers in other for early computers to do a series of multiple tasks.

Operating Systems where created to allow computers to operate and handle several tasks by themselves.
The very first operating systems helped humans load programs to computers. This was previously done by hand.
Now computers could be given batched of sequential task to do instead of waiting to be handed another task by humans.(Batch Processing)

Operating Systems where created to bridge the gap between software programs and the hardware.

Operating Systems provided API's like device drivers for software developers. OS's did most of the heavy lifting.

The invention of the Atlas Supervisor in 1962 introduced scheduling (running several programs at the same time on a single CPU) alongside batch processing (loading programs automatically).

- The introduction of a scheduler allowed multitasking - one program to run calculations on the CPU, another to print out data , and yet another to read input from a punch tape.
- During multitasking/scheduling programs are allocated blocks of memory addresses and this scattered all over the system's memory. This makes it hard from a programmer to predict where your data is saved. The operating system helps solve this problem with Memory Virtualization.

## Memory Virtualization

This is the virtualization of memory locations. The actual memory location is hidden and abstracted by the operating system.

- This allows programs to have flexible memory sizes called dynamic memory allocation that appear to be continuos to them. i.e 0-999, 1000-2000 - this could be actually 1000-2000 and 8000-9000.
- Allocating dedicated memory blocks to a program allows programs to be isolated from one another. (This is an feature the operating system provides called memory protection).

## Multiprogramming / Multitasking

This is a technique that allows several tasks to be run simultaneously by giving each program a priority. The operating system would offer the CPU to the highest priority task.
Modern operating system use preemptive multitasking, where the operating system the entire scheduling, interrupting (or preempting) tasks after a predetermined time interval.

## Time Sharing and Limited Directed Execution

- This allows a computer's resources to be shared by a large number of users or programs
- A process is a unit of execution
- Quickly run one program then another
- The way the operating system safely, and effectively executes time sharing between several processes without a massive loss of data/performance is through the use scheduling method/policies/algorithms. The os allows a process to run directly on the hardware for a short amount of time then gets back control using a timer interrupt. After the time interrupt, ,the os uses the hardware scheduling method to pick what other process runs on the hardware.
- Note - the time interrupt is a hardware security feature that cannot be controlled by a software.
- If a process is stopped by the OS in other to run another process, the state of the initial running process has to be saved. This state is preserved by a context switch.

## Scheduling / Scheduler

Assumptions to make to create scheduling

- Running time is the same for all processes
- All processes arrive at the same time
- We know the processing time for the process

Metrics for measuring scheduling

- Turn-around time (how responsive your system is)
- Throughput (how quickly can we finish all the processes in the CPU)
- Responsiveness (measuring things like responsiveness i.e typing)

- Scheduling Methods / Policies
  - **Preemptive** (Makes use of a context switch to only run processes for a given time)
    - **Round Robin**
      - Fair algorithm that gives a runs every process for only a specific time quantum
      - Has a bad response time
  - **Non-Preemptive** (Ready bad for turn around time and response time because one process has to be finished before the next)
    - **FIFO** (first process in, first process out)
      - Brute-force like simple approach
      - **SJF** (shortest job first)
        - arrange the process in descending order of processing time
      - Time taken is the sum of all the processes' processing time

If a process requires an I/O event, it takes a lot of time because it has to make a system call.

## Context Switch

- Registers, Stack and Heap are used to save a process's state.

  - Registers hold data like a function's return value
  - The Stack holds things like function local variables
    - Stack is a contiguous block of memory while the heap is more dynamic.
  - The Heap holds things like global variables

- For a context switch, a process's registers and state are saved on the kernel's stack and the resume working on a process the section of the kernel stack holding the data for the previous process is popped back to the process's register.

- Programs run in two modes:
  - User mode and Kernel mode

When a running in user mode if a program want to execute instructions like writing to a file, it invokes a system call.
The system call saves the progress of the program or process, then invokes a trap which switched to kernel mode. The hardware looks in the trap handler table and directs the operating system to perform the instruction the program was trying to execute.

- Note - user mode can't instruct the OS to do specific things like changing a real memory address value with a system call. The OS inspects a system call to make sure it is valid.

Code for context switching has to be extremely fast and is mostly written in assembly

## Interrupts

- These are signals sent to the CPU by external devices, normally I/O devices. They tell the CPU to stop its current activities and execute the appropriate part of the operating system.
- This is the main reason we can use our mouse, keyboard and other input devices while very intensive programs are running on our devices. They give us control over the computer using I/O devices.

The three types of Interrupts are:

- Hardware Interrupts (i.e keyboard, trackpad etc)
- Software interrupts (made by programs when they want to make a system call)
- Traps (generated by the CPU itself to indicate that some error or condition occurred for which assistance from the operating system is needed.)

## Threads vs Processes

- Threads are lightweight, and run is a shared memory space
- Processes are generally heavyweight, and run in separate memory spaces.

Threads and Processes are scheduled by the computer.
Threads are like semi-processes. Unlike processes, threads share data and information. They do, however, have their own stack.

If two threads are accessing the same variable, and are not synchronized. If there is a context switch, the threads don't ensure they have the current value of the variable so the work done by other threads can be overwritten.
Correct behavior is harder to attain if multiple threads are sharing data.

## Concurrency

Multiple things running at the same time.

Concurrency problems are around synchronizing all the threads to preform a task in an order.

- Problems with concurrency
  - concurrent write to a varibale
  - concurrent updates from / to a variable
    - i.e multiple threads trying to add to a variable
    -

Process execution consists of a cycle of CPU execution and I/O wait

Dispatch latency - time it takes to switch between processes

CPU utilization - keep the cpu busy as possible

throughput - a measure of work by the number of processes completed per time unit

turnaround time - sum of time spent in the waiting queue, execution in the CPU, and doing I/O

- completion time -arrival time

waiting time - sum of time spent in the ready queue

- turn around time - burst time

arrival time - when a process enters the ready queue

response time - when a process is first scheduled - arrival time

- FCFS Policy / FIFO (Non-preemptive)

  - very long waiting time (time spent in the queue)
    - avg waiting time - sum of waiting time of all processes/num of processes
  - each process has to search of matching event

- Round robin scheduling algorithm (preemptive)

  - if the process burst time > time quantum , got the next process

- Multi level feedback queue partitions the ready queue into several queues

  - each queue has it's own algorithm
  - there is scheduling among all queues
  - allows a process to move between queues.
  - if a process uses too much time it would be moved to a lower priority queue.
  - a process that waits too long in a lower priority queue may be moved to a higher-priority queue
  - uses both rr and fcfs
    - use a random qunatum for the rrs
  - seperates process with diffrent cpu-burst characteristics

- function names - roundRobin, FIFO, mlfq
- Process control is available in the form of signals, which can cause jobs to stop, continue, or even terminate.

- make a cpu class (in go) with scheduler functionality
- make an os class
- make a shell class

shell.py
from utils import shellName, currStatus, shellTextColor, clearConsole, getInput, shellVersion
from main import handleCmds

utils.py
from classes.blockedQ import BlockedQ
from classes.ioQ import IOQ

main.py
from classes.osPcb import OsPcb
from classes.mixedPcb import MixedPcb
from classes.cpuBoundPcb import CpuPcb
from classes.interactivePcb import InteractivePcb
from utils import \*

shellConfig.py

used when you print an object like so - print(proccess1)
def **str**(self):
return '|ID:{:3d}| Arrival Time:{:3d}| Burst Time:{:3d}|'.format(self.pid,self.arrival,self.burst)
