dfuzz
======

dfuzz - automatic daemon configuration fuzzer. Rather than
being a fuzzer itself, dfuzz is a wrapper for other simple fuzzers
solving few common flaws which makes automated testing a bit difficult.

Although its primary targets are configuration files, it is possible
to use dfuzz to fuzz any input files.

The main problems dfuzz solves are:
 - alpha versions of fuzzers - most of the fuzzers are just alpha versions which are no longer developed or maintained
 - common format - no need to understand how to use every single underlying fuzzer
 - customizable monitoring and automatic error analysis
 - straightforward specification of what to test and which file to supply to the target
 - combination of mutation and generation of fuzzed files

Requirements
-------------
 - python >= 2.6
 - fuzzer (zzuf, autodafé, ...)
 - gdb, valgrind (both are optional)

Features
----------
 - independent of underlying fuzzer
 - highly configurable
 - built to be extendible
 - automation friendly

Supported fuzzers
------------------
 - zzuf (mutation)
 - autodafé (generation)
 - plain (debugging purposes)

Usage
------
 - install requirements
 - install dfuzz (for example easy_install dfuzz)
 - create a working directory
 - supply fuzz.conf file (sample follows)
 - according to the modules you want to use, create mut or gen directory in your working directory and supply a file to fuzz or a template to use
 - run dfuzz -d -o `name_of_the_working_directory`
 - observe output
 - if everything is fine remove the -d and -o options and run the command again
 - check the samples directory created in your working directory
 - use included incident_viewer to browser incidents if there are any

Complete documentation in docs directory.

Sample fuzz.conf file ::

        [global]
        binary=libvirtd
        args=-f FUZZED_FILE --verbose
        threads = 1
        timeout = 2

        generation  = 0
        mutation    = 1
        combination = 0

        [generation]
        modules  = dfuzz.gen.autodafe
        priority = high

        [mutation]
        modules = dfuzz.mut.zzuf; dfuzz.mut.plain
        priority = high

        [combination]
        modules = dfuzz.comb.simple
        priority = low

In it's simplest form, dfuzz can be used as
a zzuf wrapper with enhanced detection and reporting
capabilities.
