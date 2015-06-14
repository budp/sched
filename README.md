#Explanation
`sched` is a little Python framework for scheduling jobs to be run on remote systems. It depends on the [Fabric](http://www.fabfile.org/) module for executing remote shell commands, and otherwise only uses the standard library. `sched` accepts new jobs by running the script via the command line. It also allows removing or viewing previously scheduled jobs. `sched` uses the UNIX `at` utility to automatically run scheduled jobs. `sched` uses pickling to store it's state when the program is closed. To access information about jobs that are run automatically, there is logging written to the file `job_history.log`.

#Usage
Scheduling a new job with `sched` takes at minimum a command and a time to execute that command. The time parameter can be specified in any format that is supported by the UNIX `at` utility, and commands can be anything executable by a shell. If no parameters for a remote shell are specified, it defaults to the local shell.

```
$ python sched.py --method=add --command='echo Hello World' --time='now + 1 minute'
```

It also has a number of options to support more powerful commands, for executing arbitrary jobs on remote systems at a specified time.

```
$ python sched.py --method=add --command='sh my_script.sh' --time='2:30 PM 9/21/2015' --filepath='/dir/where/output/goes/' --user=myusername --host=mysshserver.com --password=youllneverguess```
```
