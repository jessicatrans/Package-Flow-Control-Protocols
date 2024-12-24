## Implementing UDP Ping Client & Iperf Client
### UDP Ping Client
- UDP Ping client will send 10 pings to the pong server, and program will output the number of times the message is sent.
- Calculate:
  - The total number of ping/pong packets lost.
  - The total number of pong packets received.
  - RTT of each ping.
  - Overall minimum, maximum, average, and sum of RTT for 10 pings.
 
### UDP Iperf Client
- UDP Iperf client sends the message to the Iperf Server. As a response, the client will receive a text file from Iperf Server. Your UDP client should stop receiving the data from the server when target file size is reached.
  
## Implementing HTTP Client
### Non-Persistent HTTP
### Persistent HTTP
