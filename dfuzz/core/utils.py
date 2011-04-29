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
