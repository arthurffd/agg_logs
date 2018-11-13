# coding: utf-8

import os
import pandas as pd
from pathlib import Path
import re
import concurrent.futures


# Method to process http logs from a server specific directory, separating and generating temporary files by userid.
def process_logs_server(server_dir):
    print('Processing log files from server: ' + server_dir.name)
   
    # create a list with all log files in the server
    file_list = []
    for root, dirs, files in os.walk(server_dir):
        for filename in files:
            if filename.endswith('.log'):
                file_list.append(os.path.join(root, filename))
    
    # Regular expression to parse the server logs (apache log format)
    regex = '^(\S+)\s-\s-\s\[([\w:/]+\s[+\-]\d{4})\] "(\S+\s?\S+?\s?\S+)?" (\d{3}|-) (\d+|-)\s?"?[^"]*"?\s?"?([^"]*)?"$'
    # config and read all the files into dataframes:
    col_names = ['start', 'ip', 'datetime', 'command', 'status', 'bytes', 'userid', 'end']
    df_list = [pd.read_table(file, sep=regex, engine='python', names = col_names).assign(filename=os.path.basename(file)) for file in file_list]
    # concatenate all dataframes:
    dfx = pd.concat(df_list, ignore_index = True)
    dfx.dropna(axis = 'columns', how = 'all', inplace=True)
    # sort data by userid and datetime
    dfx = dfx.sort_values(by=['userid', 'datetime'])
    
    # setup files output    
    temp_dir = server_dir.resolve().parent
    temp_dir = temp_dir / 'temp'
    file_sufix = '_' + server_dir.name
    
    # group dataframe by userid and generate a file by each user    
    for i, g in dfx.groupby('userid'):
        g.to_csv( temp_dir / '{}{}.tmp'.format(i, file_sufix), header=False, index_label=False, sep=';', index = False)

    return(temp_dir)
    # consolidate all files in one, by server
    #dfx.to_csv(os.path.join(my_dir.parents[0], "consolidate_" + my_dir.name + '.log'), index=False)


# Method to process temporary log files from alls servers from a specific userid, merging files from all servers in an unique file for the userid.
def merge_logs_user(v_user):
    # setup directories:
    temp_dir = Path().resolve() / 'http_logs' / 'temp' # input dir
    dest_dir = Path().resolve() / 'http_logs' / 'user_logs' # output dir
    #print('Merging files from user: ' + v_user)

    # look for user temporary files and generates a list with them
    file_list = []
    for root, dirs, files in os.walk(temp_dir):
        for filename in files:
            if filename.startswith(v_user) and filename.endswith('.tmp'):
                file_list.append(os.path.join(root, filename))

    # prepares dataframe and read files from list:                  
    col_names = ['ip', 'datetime', 'command', 'status', 'bytes', 'userid', 'file_name'] 
    df_list = [pd.read_csv(file, delimiter=';', names = col_names) for file in file_list]
    # concatenate dataframes
    dfx = pd.concat(df_list, ignore_index = True)
    # sort lines by time ascending
    dfx = dfx.sort_values(by=['datetime'])
    
    # prepares output file
    v_user_file = v_user[7:] + '_final.log'
    # save dataframe into merged file
    dfx.to_csv( dest_dir / v_user_file, header=False, index_label=False, sep=';', index = False)
 
    return(v_user_file)
    
    

def main():
    # Create a pool of processes. By default, one is created for each CPU in your machine.
    print('Starting application...' )    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # setup directories
        x_dir = Path().resolve() / 'http_logs'
        
        # setup temporary directory
        if not os.path.exists(x_dir / 'temp'):
            os.mkdir(x_dir / 'temp')
        temp_dir = x_dir / 'temp'
        
        # setup output directory
        if not os.path.exists(x_dir / 'user_logs'):
            os.mkdir(x_dir / 'user_logs')            
        user_dir = x_dir / 'user_logs'
    
        # Get a list of servers (directories) to process
        servers_list = []    
        for x in next(os.walk(x_dir))[1]:
            if x != 'temp' and x != 'user_logs':
                servers_list.append(x_dir / x)

        # Process the list of files, but split the work across the process pool calling process_logs_server in parallel for each server
        for server, tmp in zip(servers_list, executor.map(process_logs_server, servers_list)):
            print(" The log files from ", server.name, "  were processed and staged in directory: ", tmp)

        # Get users list from files in temp dir to merge them
        user_list = []
        v_regex = re.compile(r'(userid=[a-z 0-9 /-]*).*')
        for file in os.listdir(temp_dir):
            if file.startswith('userid') and file.endswith('.tmp'):
                user_list.append(v_regex.match(file)[1])

        # keep only unique user in the list
        user_list = list(set(user_list))

        # parallel merge log files by user
        for user, file in zip(user_list, executor.map(merge_logs_user, user_list)):
            print(" Finished merging log files from ", user )

        # delete temp dir    
        import shutil
        shutil.rmtree(temp_dir)
        
        print("Finished, logs by userid can be checked in: http_logs/user_logs")

        

if __name__ == '__main__':
    main()




