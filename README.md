fingerd-multiple-hosts
======================

Simple finger server, to be run through inetd, it is both server and config file :P
Edit the python list at th start of the file to add / remove hosts.
Extra hosts must be running a fingerd that produces output identical to the normal finger command, xfingerd works fine.
I made this because I couldn't find a decent alternative.
