structs = {
    "dirent": {
        "fields": ['d_name'],
        "field_format": ["%s"]
    },
    "spwd": {
        "fields": ['sp_namp',
                   'sp_pwdp',
                   'sp_lstchg',
                   'sp_min',
                   'sp_max',
                   'sp_warn',
                   'sp_inact',
                   'sp_expire',
                   'sp_flag'],
        "field_format": ['%s', '%s', '%d', '%d', '%d', '%d', '%d', '%d', '%ld']
    },
    "passwd": {
        "fields": ['pw_name',
                   'pw_passwd',
                   'pw_uid',
                   'pw_gid',
                   'pw_gecos',
                   'pw_dir',
                   'pw_shell'],
        "field_format": ["%s", "%s", "%d", "%d", "%s", "%s", "%s"]
    },
    "utsname": {
        "fields": ['sysname',
                   'nodename',
                   'release',
                   'version',
                   'machine'],
        "field_format": ["%s","%s","%s","%s","%s"]
    },
    "timespec": {
        "fields": ['tv_sec', 'tv_nsec'],
        "field_format": ["%ld", "%ld"]
    }
}
