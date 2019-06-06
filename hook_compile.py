import re
import yaml

hook_content = '''
#include <stdio.h>
#include <dlfcn.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

'''

trace_file = './log_profile'

def include(api):
    pass

def make_typedef(api):
    typedef = f"typedef {api['return']} (*{api['name'].upper()}) "
    param_types = [re.search('\[(.*)\]', param).group(1) for param in api['inputs']]
    typedef += '(' + ", ".join(param_types) + ');\n'

    return typedef

def make_api_params(api):
    params = ", ".join(api['inputs']).replace('[', '').replace(']', '')
    params_name = [input.split(' ')[-1] for input in api['inputs']]
    params_format = [format for format in api['input_format']]

    return params, params_name, params_format

def make_return(api):
    return_type = api['return']
    declare_var = f"{return_type} ret"

    # check if return is struct
    return_data = ''
    if 'return_struct' in api:
        # return filed in struct
        if api['return_struct'] in []:
            return_data = ''
    else:
        return_data = f'"[{api["return_format"]}] ", ret'

    return declare_var, return_data

def make_func(api):
    name = api['name']
    params, params_name, params_format = make_api_params(api)
    declare_var, return_data = make_return(api)

    params_map = []
    logged_params = []
    for idx, p_name in enumerate(params_name):
        # check if format is null, it means struct
        if params_format[idx]:
            logged_params.append(p_name)
            params_map.append(f"{p_name}={params_format[idx]}")

    if logged_params:
        trace = f'"{name} {",".join(params_map)}\\n", {", ".join(logged_params)}'
    else:
        trace = f'"{name}\\n"'

    # void param
    if len(params_name) == 1 and params_name[0] == '[void]':
        params_name = []

    func = f'''
{api['return']} {name}({params}) {{
    char log[80];
    char return_data[50];
    {declare_var};

    int my_fd;
    my_fd = open("{trace_file}", O_WRONLY | O_CREAT | O_APPEND);

    void *handle = NULL;
    {name.upper()} old_func = NULL;

    handle = dlopen("libc.so.6", RTLD_LAZY);
    old_func = ({name.upper()}) dlsym(handle, "{name}");
    ret = old_func({",".join(params_name)});

    // return data
    printf({return_data});
    sprintf(return_data, {return_data});
    write(my_fd, return_data, strlen(return_data));

    // function name and params
    printf({trace});
    sprintf(log, {trace});
    write(my_fd, log, strlen(log));
    close(my_fd);

    return ret;
}}\n
'''

    return func

def main():
    global hook_content
    with open('./api.yml', 'r') as f:
        api_conf = yaml.safe_load(f)

    for type, apis in api_conf.items():
        if type != 'string':
            continue
        for api in apis:
            hook_content += make_typedef(api)
            hook_content += make_func(api)

    with open('./hook.c', 'w') as f:
        f.write(hook_content)

if __name__ == "__main__":
    main()
