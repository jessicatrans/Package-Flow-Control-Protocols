from socket import *
import time, random

# Preparing the socket
# Pong Server
IP_Address = "173.230.149.18"
port = 12000

# Create UDP client socket, specify that it is IPv4
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Variables
successPackets = 0          # number of successful packets
stored_RTTs = []            # array of round trip times
totalRTT = 0                # sum
minRTT = 0
maxRTT = 0
avgRTT = 0
timeout_count = 0
temp = 0
timeout_seconds = 10
timeout_upperLimit = 10     # 10 minutes
packets_lost = 0
i = 1
count = 0

# Create UDP client socket, specify that it is IPv4
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Will wait for 10 seconds, if time exceeds that then packet will be considered lost
clientSocket.settimeout(timeout_seconds)

# Ping 10 times
while i <= 10:
    curTime = time.time()
    message = "ping"

    try:       
        # work on what to send the server with
        clientSocket.sendto(message.encode(), (IP_Address, port))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print("The current time is: ", curTime, " and this is the message number: ", str(i))
        print("Uppercase Message from the Server: ", modifiedMessage)

        endTime = time.time()

        # Calculate the RTT in milliseconds
        rtt = endTime - curTime
        # Print the Round Trip Time
        print("The Round Trip Time is: ", rtt, "seconds")
        stored_RTTs.append(rtt)
        totalRTT += rtt     # Update sum of round trip times
        i += 1
    except:
        # Client does not receive the message from the server
        if (timeout_seconds >= (timeout_upperLimit * 60)): 
            packets_lost += 1
            i += 1
            count = 0
            timeout_count = 0
            continue
        if (count == 0):
            time.sleep(timeout_seconds)
            count += 1
            continue
        if (count == 1):
            timeout_count = 1
            # Exponential Backoff Function
            timeout_seconds = timeout_seconds * (pow(2, timeout_count)) + random.uniform(0,1)
            time.sleep(timeout_seconds)

successPackets = 10 - packets_lost

# Output in terminal
print("the program is done")
print("Stored RTTs are: ", stored_RTTs)
print("Total number of successful packets is: ", successPackets)

# Store list of RTTs to find max and min
stored_RTTs.sort()      # sort the array of round trip times
maxRTT = stored_RTTs[successPackets-1]
minRTT = stored_RTTs[0]
avgRTT = totalRTT/successPackets
print("Max RTT is: ", maxRTT, "seconds")
print("Min RTT is: ", minRTT, "seconds")
print("Sum of all RTTs is: ", totalRTT, "seconds")
print("Average Round Trip Time is: ", avgRTT)
print("Total number of packet lost is: ", packets_lost)

clientSocket.close()