import re
import yaml
from struct import structs


trace_file = './log_profile'
hook_content = '//This code is auto generated by hook_compile.py\n'
headers = set([
    'stdio.h',
    'dlfcn.h',
    'fcntl.h',
    'string.h'
])

def make_header(api):
    global headers

    if type(api['include']) != str:
        for header in api['include']:
            headers.add(header)
    else:
        headers.add(api["include"])


def make_typedef(api):
    typedef = f"typedef {api['return']} (*{api['name'].upper()}) "
    param_types = [re.search('\[(.*)\]', param).group(1) for param in api['inputs']]
    typedef += '(' + ", ".join(param_types) + ');\n'

    return typedef

def parse_params(api):
    params = [input.replace('[', '').replace(']', '') for input in api['inputs']]
    # params = ", ".join(api['inputs']).replace('[', '').replace(']', '')
    params_name = [input.split(' ')[-1] for input in api['inputs']]
    params_format = [format for format in api['input_format']]

    return params, params_name, params_format


def make_struct(struct_name, struct_var = None):
    var_map = []
    var_names = []

    this_struct = structs[struct_name]
    for idx, field in enumerate(this_struct['fields']):
        var_map.append(f'{field}={this_struct["field_format"][idx]}')

        # check sturct is used for return or params
        if not struct_var:
            var_names.append(f'ret -> {field}') # return
        else:
            var_names.append(f'{struct_var} -> {field}') # param

    format_str = f'"[{",".join(var_map)}] ", {",".join(var_names)}'
    return format_str, var_map, var_names

def get_struct_name(struct):
    if 'struct' in struct:
        struct_name = re.search('struct (.*)\*', struct).group(1)
    else:
        struct_name = struct.replace('*', '')

    struct_var = re.search('\*\s(.*)', struct).group(1)
    return struct_name, struct_var

def make_return(api):
    return_type = api['return']

    if return_type == 'void':
        return '', ''

    declare_var = f"{return_type} ret;"
    # check if return is struct
    return_data = ''
    return_check = '''(ret != 0)'''

    if 'return_struct' in api:
        # return filed in struct
        return_check = '(ret == NULL)'
        struct_name, _ = get_struct_name(return_type)
        if struct_name in structs:
            return_data, _, _ = make_struct(struct_name)
    else:
        return_data = f'"[{api["return_format"]}] ", ret'
        if '*' in return_type:
            return_check = '(ret == NULL)'

    return declare_var, return_data, return_check

def make_params(api_name, params, params_name, params_format):
    var_map = []
    var_names = []

    for idx, p_name in enumerate(params_name):
        # append multi fields from struct
        if params_format[idx] == 'struct':
            struct_name, struct_var = get_struct_name(params[idx])
            _, map, names = make_struct(struct_name, struct_var)

            var_map += map
            var_names += names
        # check if format is null, it means struct
        elif params_format[idx]:
            var_names.append(p_name)
            var_map.append(f"{p_name}={params_format[idx]}")

    if var_names:
        trace = f'"{api_name} {",".join(var_map)}\\n", {", ".join(var_names)}'
    else:
        trace = f'"{api_name}\\n"'

    return trace

def make_func(api):
    name = api['name']

    declare_var, return_data, return_check = make_return(api)
    params, params_name, params_format = parse_params(api)
    trace = make_params(name, params, params_name, params_format)

    # format params input string: char* name, int mode
    params = ", ".join(params)

    # void param
    if len(params_name) == 1 and params_name[0] == '[void]':
        params_name = []

    ret = f'''
    ret = old_func({",".join(params_name)});
    if {return_check} return ret;'''
    return_value = 'ret;'

    # void return
    if not return_data:
        return_data = '"[-] "'
        ret = ''
        return_value = f'old_func({",".join(params_name)});'

    func = f'''
{api['return']} {name}({params}) {{
    char log[256];
    char return_data[256];
    {declare_var}

    int my_fd;
    my_fd = open("{trace_file}", O_WRONLY | O_CREAT | O_APPEND);

    void *handle = NULL;
    {name.upper()} old_func = NULL;

    handle = dlopen("libc.so.6", RTLD_LAZY);
    old_func = ({name.upper()}) dlsym(handle, "{name}");
    {ret}

    // return data
    printf({return_data});
    sprintf(return_data, {return_data});
    write(my_fd, return_data, strlen(return_data));

    // function name and params
    printf({trace});
    sprintf(log, {trace});
    write(my_fd, log, strlen(log));
    close(my_fd);

    return {return_value}
}}\n
'''
    return func

def main():
    global hook_content, headers
    with open('./api.yml', 'r') as f:
        api_conf = yaml.safe_load(f)

    for api_type, apis in api_conf.items():
        if api_type != 'others':
            continue
        for api in apis:
            make_header(api)
            hook_content += make_typedef(api)
            hook_content += make_func(api)

    with open('./hook.c', 'w') as f:
        f.write('\n'.join([f'#include <{h}>' for h in headers]))
        f.write('\n')
        f.write(hook_content)

if __name__ == "__main__":
    main()
