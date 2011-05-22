Instalation
===========

Source
-------

Install from source by running `python setup.py install`
in main directory.


Pypi
-----

To install from Python Package Index use
`pip install dfuzz` or `easy_install dfuzz`.


Requirements
-------------

One of:
 - zzuf - http://caca.zoy.org/wiki/zzuf
 - autodafe - http://autodafe.sourceforge.net/


Optional tools
---------------

 - GDB - GNU Debugger - probably present in your distribution
 - Valgrind - memory analyzer - http://valgrind.org/
 - no_commets - comment stripping utility - https://github.com/sorki/no_comments


Usage
======

Basic usage
------------

 - Create work directory (referenced as `work_dir`)
 - In the directory, create `fuzz.conf` file
 - Set two values in the section named `[global]`
    - `binary = binary_to_test` where `binary_to_test` is in located in your work directory or in your `$PATH`
    - `args = -f FUZZED_FILE` - arguments passed to the specified binary. `FUZZED_FILE` is replaced with proper path to file which is currently being fuzzed

 - Create `work_dir/mut` subdirectory
 - Put configuration file which should be mutated to the `work_dir/mut` subdirectory
 - Run `dfuzz` with `--debug` and `--debug_output` parameters::

         dfuzz --debug --debug_output <path_to_work_dir>

 - Check output for errors
 - Check `work_dir/samples` directory
   - open one of the samples and check whether the output is correct
   - try to run one of the samples with `run_XY` script


This procedure will test specified binary with 10 mutated files.
The files are mutated with zzuf. If everything is fine, we
can start real testing.

 - Open the `fuzz.conf` file and add the following section::

           [mutation]
           modules = dfuzz.mut.zzuf
           priority = high

 - This will cause the removal of 10 mutations limit
 - Run `dfuzz` again, now without debugging options::

         dfuzz <path_to_work_dir>

Now `dfuzz` will test specified binary 10k times with
10k different mutations. If it finds any incidents
it will report the fact at the end of the test run.
If there are any incidents, run `incident_viewer` tool::

        incident_viewer <path_to_incidents_subdir>

This completes basic usage tutorial.

Using Autodafe
---------------

To take advantage of this tool you have to create
`gen` subdirectory the same way as `mut` subdirectory.
Then you have to create an Autodafe template and put it into
the `gen` subdirectory. You can now rerun the testing - `dfuzz`
will detect the existence of the template and will run Autodafe
generation routines (along with zzuf testing).


Disabling fuzzing methods
--------------------------

The following part of the configuration file illustrates the way
how to enable or disable one of the fuzzing methods::

        [global]
        generation  = 1
        mutation    = 1
        combination = 0

By default, combination will combine Autodafe and Zzuf modules provided
that there is `comb` subdirectory present in your work dir and there
is an Autodafe template to work with.


Method customization
----------------------

Each of the fuzzing methods is highly configurable. It is
possible to set which classes to use, set their parameters and
priority of the method. Default configuration follows ::

        [generation]
        modules  = dfuzz.gen.autodafe
        priority = low

        [mutation]
        modules = dfuzz.mut.zzuf_10
        priority = high

        [combination]
        modules = dfuzz.comb.simple
        priority = low

Class `dfuzz.mut.zzuf_10` will create 10 mutations of the input.
It's a subclass of `dfuzz.mut.zzuf` which is used as a main class
for fuzz testing. Class `dfuzz.mut.zzuf` accepts three parameters:

 - minimal percentage of bytes to fuzz
 - maximal percentage of bytes to fuzz
 - number of mutations to create (with different seeds)

Best illustrated by an example:::

        [mutation]
        modules = dfuzz.mut.zzuf(0.01, 0.2, 500)
        priority = high

This will set the range of the bytes to fuzz to 0.1% to 0.2%
and will produce 500 different mutations of the input.

Combination class `dfuzz.comb.simple` accepts
two parameters - classes to combine. Its default behaviour
is illustrated by following example::

        [combination]
        modules = dfuzz.comb.simple(dfuzz.gen.autodafe, dfuzz.mut.zzuf_10)
        priority = low

So by default class combines generation of files by Autodafe with their
mutation by Zzuf. To save time, only 10 mutation of each file are done.


Priorities & threading
^^^^^^^^^^^^^^^^^^^^^^

Priority of each method can be set to `low` or `high`. High priority methods
will precede low priority ones.

It's also possible to run multiple fuzzers simultaneously in threads.
Number of threads is specified by `threads = X` option. Default
setting is `threads = 1` as most of the Linux daemons require
open ports or exclusive access to files.


Supplying plain files
^^^^^^^^^^^^^^^^^^^^^^^

If you posses test files which are/were problematic
you can supply them during the testing directly without
prior fuzzing. Class for the job is `dfuzz.mut.plain`
which only copies its input to the output directory.


Creating new wrapper/fuzzer class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Modularity and dynamic module loading allows
simple creation of fuzzers or wrappers for
existing fuzzers.

This is done by subclassing `dfuzz.core.wrapper.DfuzzWrapper`.
New class has to implement following methods:

 - `__str__` - which should return short name of the class
 - `method` - which returns one of `mut/gen/comb` method identifiers
 - `set_up` - accepts input file path and parameters supplied via config
 - `run` - returns generator which yields full paths to output file

When creating new fuzzer or wrapper it's best to look at one
of the existing classes.


Using external tools
---------------------

`Dfuzz` can take an advantage of two external tools:

 - GDB - GNU Debugger
 - Valgrind - runtime memory analyzer

To enable these tools put following snippet into your `fuzz.conf` file::

        [core]
        target=dfuzz.core.target.TimedValgrindTarget
        incident=dfuzz.core.incident.TimeValgrindIncident
        incident_handler=dfuzz.core.handler.GDBFileIncidentHandler

Again, modularity allows you to use your own classes.
Implementation of target runners or handlers is not covered in this guide.


Handling timeouts
^^^^^^^^^^^^^^^^^^

Default timeout for single test is set to 3 seconds. If it is exceeded
tested application is killed.

It is possible to record timeouts as incident with `timeout_as_incident = 1` option.


Other configuration options
----------------------------

Documented with comments next to their default value::


        [global]
        num_samples = 2 ; number of output samples to store

        [file]
        use_no_fuzz = 0 ; append/prepend/0 ; turns on the inclusion of no_fuzz_file
        ; specified in input section. Values are self explanatory.
        ; This file is inserted to the output _after_ fuzzing process.

        [input]
        no_fuzz_file = no_fuzz ; name of no_fuzz file

        gen_dir  = gen ; generation templates directory
        mut_dir  = mut ; mutation inputs directory
        comb_dir = comb ; combination inputs directory

        gen_dir_mask  = * ; masks for respective directory, used to filter files
        mut_dir_mask  = * ; same way the shell works
        comb_dir_mask = *

        [output]
        tmp_dir = tmp ; temporary directory, used to store outputs
        samples_dir = samples ; samples directory

        incidents_dir    = incidents ; directory where the incidents are stored
        incident_format  = U ; `U` - uuid `I` - #nth incident

        ; filenames of the files which are generated
        ; by default incident handler
        incident_info    = info
        incident_input   = input
        incident_stdout  = stdout
        incident_stderr  = stderr
        incident_minimal = input_minimal
        incident_valgrind = valgrind
        incident_reproduce  = reproduce.sh
