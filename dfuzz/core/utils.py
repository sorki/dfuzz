def parse_args(str_args, mapping={'FUZZED_FILE': '%(input)s'}):
    '''
    Replace keywords with python string formatting tokens.
    '''
    for key, value in mapping.iteritems():
        str_args = str_args.replace(key, value)

    return str_args
