import os
import logging
import subprocess

def dir_integrity(cfg_obj):
    '''
    Ensure `work_dir` integrity, update `cfg_obj` paths
    to absolute paths if necessary, create log, incidents
    and tmp sub directories
    '''

    work_dir = cfg_obj.work_dir

    sub_dirs = ['gen_dir', 'mut_dir', 'comb_dir', 
        'log_dir', 'incidents_dir', 'tmp_dir']

    if not os.access(work_dir, os.W_OK):
        logging.error('Work dir "%s" must be writable' % work_dir)
        return False

    failure = False

    for d in sub_dirs:
        path = getattr(cfg_obj, d)
        abspath = path
        if path[0] != '/':
            abspath = os.path.join(work_dir, path)
            setattr(cfg_obj, d, abspath)

        if d in ['log_dir', 'incidents_dir', 'tmp_dir']:
            if not os.path.isdir(abspath):
                logging.info('Creating dir: %s [%s]' % (d, path))
                os.mkdir(abspath)

            if not os.access(abspath, os.W_OK):
                logging.error('No write perms for: %s [%s]' %
                    (d, abspath))
                failure = True

        if os.path.isdir(abspath) and not os.access(abspath, os.R_OK):
            logging.error('No read perms for: %s [%s]' % (d, abspath))
            failure = True

    modes = ['generation', 'mutation', 'combination']
    dirs =  ['gen_dir', 'mut_dir', 'comb_dir']

    for mode,modedir in zip(modes, dirs):
        if getattr(cfg_obj, mode):
            if not os.path.isdir(getattr(cfg_obj, modedir)):
                setattr(cfg_obj, mode, False)
                logging.warning('%s option is set to 1 but no '
                    '%s [%s] found, unsetting' % (mode, modedir,
                    getattr(cfg_obj, modedir)))


    return not failure

def find_binary(binary_str, work_dir):
    '''
    Try to find specified binary in:
      - `work_dir` (specified in fuzz.conf)
      - / (if it's already an absolute path)
      - $PATH
    Return absolute path to binary, None if not found.
    '''
    def valid(path):
        return os.access(path, os.R_OK | os.X_OK)

    # relative to work_dir
    test_path = os.path.join(work_dir, binary_str)
    if os.path.isfile(test_path):
        if valid(test_path):
            return test_path

    # absolute
    test_path = binary_str
    if os.path.isfile(test_path):
        if valid(test_path):
            return test_path

    # $PATH
    pr = subprocess.Popen('which "%s"' % binary_str, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    retcode = pr.wait()
    if retcode == 0:
        test_path = pr.communicate()[0].strip()
        if valid(test_path):
            return test_path

    return None

def check_required(cfg_obj):
    '''
    Check for required values in cfg object.
    '''
    req_fields = ['binary', 'args']
    for r in req_fields:
        if not hasattr(cfg_obj, r):
            return False

        if len(getattr(cfg_obj, r)) == 0:
            return False

    return True

def value_validator(cfg_obj):
    '''
    Validate values in cfg object.

    Returns False if there are any
    invalid values.
    '''

    va_dict = {
        'use_no_fuzz' : [False, 'prepend', 'append'],
        'threads'     : int,
        'timeout'     : float,
        'generation'  : int,
        'mutation'    : int,
        'combination' : int,
        'generation_priority'  : ['low', 'high'],
        'mutation_priority'    : ['low', 'high'],
        'combination_priority' : ['low', 'high'],
    }

    # TODO (normal): validate incident_format


    for k,v in va_dict.iteritems():
        val = getattr(cfg_obj, k)
        if type(v) == list:
            if val not in v:
                logging.error('Config parse error. Property "%s"'
                    ' set to undefined value "%s".'
                    ' Valid values: "%s"',
                    k, getattr(cfg_obj, k), '" "'.join(v))
                return False
        elif v in [int, float]:
            try:
                v(val)
            except ValueError as e:
                logging.error('Config parse error. Property "%s"'
                    ' has wrong type. Expected type: "%s"',
                    k, v)
                return False

    return True
