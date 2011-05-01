import uuid
import logging

def parse_args(str_args, mapping={'FUZZED_FILE': '%(input)s'}):
    '''
    Replace keywords with python string formatting tokens.
    '''
    for key, value in mapping.iteritems():
        str_args = str_args.replace(key, value)

    return str_args

def handle_no_fuzz(input_path, no_fuzz_path, mode):
    '''
    Open and append/prepend `no_fuzz_path` file
    to `input_path` file.
    '''
    with open(no_fuzz_path) as nf:
        nf_contents = nf.read()

    if mode == 'append':
        with open(input_path, 'a') as f:
            f.write(nf_contents)
    else:
        with open(input_path, 'r') as orig:
            orig_content = orig.read()

        with open(input_path, 'w') as rew:
            rew.write(nf_contents)
            rew.write(orig_content)

def get_class_by_path(str_path):
    module_name, cls_name = str_path.rsplit('.', 1)
    try:
        mod = __import__(module_name, fromlist=['a'])
    except ImportError:
        logging.error('No such module: "%s"', module_name)
        return False

    if hasattr(mod, cls_name):
        cls = getattr(mod, cls_name)
        return cls

    logging.error('Module "%s" has no "%s" class.', module_name,
        cls_name)
    return False


def parse_incident_fmt(cfg):
    fmt = cfg.incident_format
    iid = str(cfg.num_incidents)
    uid = str(uuid.uuid4())
    fmt = fmt.replace('U', uid)
    fmt = fmt.replace('I', iid)
    return fmt
