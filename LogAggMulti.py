# coding: utf-8

import os
from pathlib import Path
import pandas as pd
import re
import concurrent.futures



def process_logs_server(my_dir):
    file_list = []
    print('Processando agora server: ' + my_dir.name)
    for root, dirs, files in os.walk(my_dir):
        for filename in files:
            if filename.endswith('.log'):
                file_list.append(os.path.join(root, filename))
    
    regex = '^(\S+)\s-\s-\s\[([\w:/]+\s[+\-]\d{4})\] "(\S+\s?\S+?\s?\S+)?" (\d{3}|-) (\d+|-)\s?"?[^"]*"?\s?"?([^"]*)?"$'
    col_names = ['start', 'ip', 'datetime', 'command', 'status', 'bytes', 'userid', 'end']

    df_list = [pd.read_table(file, sep=regex, engine='python', names = col_names).assign(filename=os.path.basename(file)) for file in file_list]
    dfx = pd.concat(df_list, ignore_index = True)
    dfx.dropna(axis = 'columns', how = 'all', inplace=True)
    dfx = dfx.sort_values(by=['userid', 'datetime'])
         
    temp_dir = my_dir.resolve().parent
    temp_dir = temp_dir / 'temp'
    file_sufix = '_' + my_dir.name
        
    for i, g in dfx.groupby('userid'):
        g.to_csv( temp_dir / '{}{}.tmp'.format(i, file_sufix), header=False, index_label=False, sep=';', index = False)

    return(dfx)        
    # consolidate by server
    #dfx.to_csv(os.path.join(my_dir.parents[0], "consolidate_" + my_dir.name + '.log'), index=False)



def merge_logs_user(v_user):
    temp_dir = Path().resolve() / 'http_logs' / 'temp'
    dest_dir = Path().resolve() / 'http_logs' / 'user_logs'
    file_list = []
    print('Consolidando arquivos: ' + v_user)

    for root, dirs, files in os.walk(temp_dir):
        for filename in files:
            if filename.startswith(v_user) and filename.endswith('.tmp'):
                file_list.append(os.path.join(root, filename))

    col_names = ['ip', 'datetime', 'command', 'status', 'bytes', 'userid', 'file_name'] 
    df_list = [pd.read_csv(file, delimiter=';', names = col_names) for file in file_list]
    
    dfx = pd.concat(df_list, ignore_index = True)
    dfx = dfx.sort_values(by=['datetime'])
    
    v_user_file = v_user[7:] + '_final.log'
    
    dfx.to_csv( dest_dir / v_user_file, header=False, index_label=False, sep=';', index = False)
 
    return(v_user_file)
    

def main():

    # MAPPER
    # Create a pool of processes. By default, one is created for each CPU in your machine.
    with concurrent.futures.ProcessPoolExecutor() as executor:
    
        # Get a list of files to process
        servers_list = []
        x_dir = Path().resolve() / 'http_logs'
        
        if not os.path.exists(x_dir / 'temp'):
            os.mkdir(x_dir / 'temp')
            temp_dir = x_dir / 'temp'

        if not os.path.exists(x_dir / 'user_logs'):
            os.mkdir(x_dir / 'user_logs')            
            user_dir = x_dir / 'user_logs'
   
        for x in next(os.walk(x_dir))[1]:
            if x != 'temp' and x != 'user_logs':
                servers_list.append(x_dir / x)
            
        for server in servers_list:
            print(f"Processamento de log files para {server.name} iniciado.")    

        # Process the list of files, but split the work across the process pool to use all CPUs!
        for server, dfz in zip(servers_list, executor.map(process_logs_server, servers_list)):
            print(f" The log files from {server.name} was processed")


        # Get user list from files to merge files
        v_regex = re.compile(r'(userid=[a-z 0-9 /-]*).*')
        user_list = []
        
        for file in os.listdir(temp_dir):
            if file.startswith('userid') and file.endswith('.tmp'):
                user_list.append(v_regex.match(file)[1])

        # unique users list
        user_list = list(set(user_list))

        # parallel merge log files by user
        for user, file in zip(user_list, executor.map(merge_logs_user, user_list)):
            print(f" The log files from {user} were merged")

        # delete temp files    
        import shutil
        shutil.rmtree(temp_dir)
    

if __name__ == '__main__':
    main()


#dfx = dfx.sort_values(by=['userid', 'datetime'])
#for i, g in dfx.groupby('userid'):
#    g.to_csv(my_dir / '{}.log'.format(i), header=False, index_label=False, sep=';', index = False)


#dfx.to_csv(os.path.join(my_dir, "Consolidate.log"), index=False)



