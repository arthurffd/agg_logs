# Challenge - HTTP Logs Agregation
This is the Http logs agregation challenge: collect log files from different HTTP servers and then agreggate all files by userid, ordering by time. After processing and agreggate the application will generate one unique file by each userid.

## Purpose: 
This document contains necessary information to run the application and explain the purposes and expected results.<br />
<br />
Customer: Linx <br />
Developer: Arthur F. Flores Duarte <br />
<br />
Created Date: 2018/11/12 <br />
Last Updates:  <br />
Application developed in Python 3
<br /><br />

## How to run the application:
  1. First of all unzip LogAggMulti.zip in you environment (Ubuntu) and access directory LogAggMulti  "cd LogAggMulti";<br />
  
  2. The application already contains a sample of http server logs files, but you can add more log files in the following directories (each one represents log files from different servers):
      *  .\http_logs\server_01<br />
      *  .\http_logs\server_02<br />
      *  .\http_logs\server_03<br />
      *  .\http_logs\server_04<br /><br />
  
  3. Execute the "chmod +777 start.sh"  and "chmod +777 install.sh" to get permission for execution and then execute the scripts<br />
  
  4. Execute the script "./install.sh" to setup install of Python3 and related packages (pip, pandas, futures).<br />
  
  5. Execute the script "./start.sh" to run the application (LogAggMulti.py) .<br />
 
  6. The application will diplay some messages and after finished you can see the log files by each userid in the directory: \http_logs\user_logs\
    
## Project Files:
  ###  LogAggMulti.py - Main application: 
  Description: Process http logs from differente servers (directories) and agreggate by userids, generating one file by userid, containing all his http logs ordered by datetime.
  
  Methods:
  #### process_logs_server(server_dir)
  Description: Method to process http logs (Apache format) from a server specific directory, separating and generating temporary files by userid.<br />
  Input: server_dir (os.path) - OS Path representing a server directory containing log files;<br />
  Output: temp_dir (os.path) - OS Path - temporary directory containing the processed files by userid;<br />
  
  #### merge_logs_user(v_user)
  Description: # Method to process temporary log files from all servers from a specific userid, merging temporary files from all servers in an unique file for the userid. <br />
  Input: v_user (String) - The method will process files that belongs to the specified Userid 
  Output: v_user_file (os.file) - File containing all logs from the specified userid.
  
## Log Files
### Input Log Files sample:
Apache Log formats: https://httpd.apache.org/docs/2.4/logs.html
> 177.126.180.83 - - [15/Aug/2013:13:54:38 -0300] "GET /meme.jpg HTTP/1.1" 200 2148 "-" "userid=5352b590-05ac-11e3-9923-c3e7d8408f3a"
> 177.126.180.83 - - [15/Aug/2013:13:54:38 -0300] "GET /lolcats.jpg HTTP/1.1" 200 5143 "-" "userid=f85f124a-05cd-11e3-8a11-a8206608c529"
> 177.126.180.83 - - [15/Aug/2013:13:57:48 -0300] "GET /lolcats.jpg HTTP/1.1" 200 5143 "-" "userid=5352b590-05ac-11e3-9923-c3e7d8408f3a"

### Output Log Files sample:
The output log files will be available in the directory: \LogAggMulti\http_logs\user_logs <br />
File name will follow this standard: <userid>_final.log . Example: 5352b590-05ac-11e3-9923-c3e7d8408f3a_final.log <br />
<br />
Format layout, separated by ";" :
Host; Datetime; http command; http status; message bytes; userid; original log file name;
>177.126.180.83;14/Aug/2013:07:54:38 -0300;GET /meme.jpg HTTP/1.1;200;2148;userid=5352b590-05ac-11e3-9923-c3e7d8408f3a;0004_20130815_005.log
>177.126.180.83;14/Aug/2013:10:54:38 -0300;GET /meme.jpg HTTP/1.1;200;2148;userid=5352b590-05ac-11e3-9923-c3e7d8408f3a;0003_20130815_0034.log
>177.126.180.83;14/Aug/2013:10:55:38 -0300;GET /meme.jpg HTTP/1.1;200;2148;userid=5352b590-05ac-11e3-9923-c3e7d8408f3a;0003_20130815_0034.log
<br /><br />
