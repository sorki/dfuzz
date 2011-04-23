import os
import logging

def dir_integrity(work_dir, cfg_obj):
    '''
    Ensure `work_dir` integrity, update `cfg_obj` paths
    to absolute paths if necessary, create log, incidents
    and tmp sub directories
    '''

    sub_dirs = ['gen_dir', 'mut_dir', 'comb_dir', 
        'log_dir', 'incidents_dir', 'tmp_dir']

    if not os.access(work_dir, os.W_OK):
        logging.error('Work dir "%s" must be writable' % work_dir)
        return False

    failure = False

    for d in sub_dirs:
        path = getattr(cfg_obj, d)
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
