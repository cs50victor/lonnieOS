[x] display welcome message
[x] Version: Display the software version number for your simulator
[x] Date: Display date
[x] Exit: Exit the simulator. You should ask the user if they are sure that they want to exit.
[x] History: Display a history of the last ten commands a user used.
[x] Directory: Print a list of all the files in the simulator’s directory.At this point, you may assume that there is only one directory for the OS. This command may take some research.
[x] Help: Display help information for each command. Should be able to display a list of all commands present on the system.
[x] Aliasing: Allow the user to map different command names (i.e. renaming Exit to Quit)
[x] Batch files: Run commands from a batch file or script
[x] Set the date
[x] fix displaymsg function
[x] Add more details to welcome message 
[x] add cpu logs

[x] Make automated tests for all functions
[] add type hinting for all variables
[] do manuals



[] read turn around time - section 7.2
[] read response time - section 7.6

[] report when each process exits
[] calculate turn around time and response time for a set of processes in the CPU

[] calculate the percentage of time that the CPU is active 

[] create a on OS pcb that cannot be put in the blocked queue or completely removed
[] add a time cycle every time a process is moved to the cpu
[] modify createPcb, generate PCB, and execute
[] implement round robin
[] implement multilevel feedback queue in execute


[] Task 4 [7.2-7.6]
[] Task 5

turnaround time = time for completion


You should report these when each process exits, but also keep track of them so that you can calculate the average turnaround and response times for a set of processes when the execute command finishes.
You will also need to perform a CPU Utilization calculation. This calculation is the percentage of time that the CPU is active (has a PCB in it). To be clear, if there is nothing for the CPU to do (all current processes are blocked, waiting for events), then the CPU is not being utilized. The result of this calculation should be output when the execute function finishes running.

