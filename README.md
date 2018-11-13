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
<br /><br />

## How to run the application:
  1. First of all unzip LogAggMulti.zip and access directory LogAggMulti;<br />
  
  2. The application already contains a sample of http server logs files, but you can add more log files in the following directories (each one represents log files from different servers):
      *  .\http_logs\server_01<br />
      *  .\http_logs\server_02<br />
      *  .\http_logs\server_03<br />
      *  .\http_logs\server_04<br /><br />
  
  3. Execute the chmod +777 start.sh to get permission for execution and then execute script "./start.sh" ; <br />
  
  4. The application will diplay some messages and after finished you can see the log files by each userid in the directory: \http_logs\user_logs\
  

<br /><br />
