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
that there is `comb` subdirectory presnet in your work dir and there
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

Priority of each method can be set to `low` or `high`. High priority methods
will precede low priority ones.
