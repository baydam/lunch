# The Lunch distributed process launcher

Lunch is a distributed process launcher and manager for GNU/Linux.

With Lunch, one can launch software processes on several different computers
and make sure they keep running. This software was created to suit the needs
of new media artists for live performances and interactive installations.
It respawns the software that crash and provides a mean to manage
dependencies between running processes.

It provides the command-line lunch utility which can be invoked with a GTK+
user interface.


## USING LUNCH

Here is a quick how-to. Make sure lunch is installed first. (see INSTALL)
There should be a Lunch icon in the Application/Other Gnome menu.

Copy the "config-sample" example config file to the local ~/.lunchrc :

```
cp doc/examples/config-sample ~/.lunchrc
```

Edit the configuration file to suit your needs::

```
edit ~/.lunchrc
```

Start the lunch master::

```
lunch
```

A remote lunch-slave is started this way::

```
lunch-slave -i "xlogo"
lunch-slave "xdg-open"
```

Next, the lunch scripts controls the lunch-slave via its standard input and output. Type "help" in lunch-slave and press enter to see how the lunch-slave prompt is used by lunch. That prompt is not meant to be used directly by an operator, but rather only through lunch.

The .lunch/config file is written in the Python language and the only function needed to be called there is add_command. Here are some examples::

```
add_command(command="xlogo", env={}, identifier="xlogo")
add_command(command="mplayer /usr/share/example-content/Ubuntu_Free_Culture_Showcase/StopMotionUbuntu.ogv", env={}, identifier="mplayer")
```

Setting the user and host arguments make it be issued through SSH to a remote host::
 
```
add_command(command="xlogo", env={"DISPLAY":":0.0"}, user=_user, host="example.org", identifier="remote_xlogo")
```

See the examples for more information about this.


## Versioning

We use semantic versioning 1.0.


## Logging and PID directories

Lunch stores log files and pid files respectively in /tmp/log/lunch-$USER and /tmp/run/lunch-$USER, where $USER is
replaced by the UNIX user name of the user. When you install lunch, it creates those directories. If you want to use
lunch without installing it, you must provide the --logging-directory and --pid-directory options. Those log files
are for the lunch-slave executables only. (not the lunch master) The PID file is for the lunch master to store its
PID so that you can kill it with lunch --kill.


## LICENSE

Lunch is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later version.


## AUTHORS


- Alexandre Quessy <alexandre@quessy.net>
- Michal Seta <djiamnot@gmail.com>
- Tristan Matthews
- Vincent Granger-Pradéras

