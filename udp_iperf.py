from socket import *
import time

# Preparing the socket
IP_Address = "173.230.149.18"
port = 5006
size = 0                        # size of data received
sizeOfFile = 0
startTime = time.time()         # countdown
targetedSize = 1300000

# Create UDP client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

sendMessage = "ping"
# Work on what to send the server with
clientSocket.sendto(sendMessage.encode(), (IP_Address, port))

while True:
    data, serverAddress = clientSocket.recvfrom(4096)
    print("received %: ", round((size/targetedSize) * 100))
    # Append data into a file
    with open("File.txt", "ab") as f:
        f.write(data)
        f.write('\n'.encode())

    size += len(data)

    if (size >= targetedSize):
        sizeOfFile = size - len(data)
        print("break")
        break

# Calculate time
endTime = time.time()
duration = endTime - startTime

clientSocket.close()

# Output 
print("Time elapsed:", duration, "seconds")
print("Throughput: ", (size*8)/duration, "bps")
print("Size of file is ", sizeOfFile * 8, "bites")
print("File Downloaded")