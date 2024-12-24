from socket import *
from bs4 import BeautifulSoup
import time
import os.path

# for debugging purposes, delete ecs152.html file and images folder

# find content length from http response headers
def findContentLen(header):
    content_length = 0
    cut_here = '\r\n\r\n'

    if cut_here in header:
        temp1 = data.split('Content-length: ')      # split where it says content-length in header
        temp2 = temp1[1].split(cut_here)            # split at '\r\n\r\n'
        content_length = int(temp2[0])              # get the length and convert to int
    return content_length

# IP Address and Port Number of Server
host = "173.230.149.18"
port = 23662

# Variables
PLT_time = 0
startTime_plt = 0
endTime_plt = 0
avg_request_delay_time = 0
ATF_PLT_time = 0
startTime_atf_plt = 0
endTime_atf_plt = 0
totalATF_PLT = 0
x = 0
rps_time = 0
numOfRequests = 0

startTime_plt = time.time()

# check if ecs152a.html file exists, if not then create html file
file_exists = os.path.exists('ecs152a.html')
if not file_exists: # if false, get esc152.html file from server
    size = 0
    content_length = 0
    startTime_atf_plt = time.time()

    # create TCP socket object, IPv4
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))

    # client sends request to server
    request = "GET /ecs152a.html HTTP/1.1\r\nHost: 173.230.149.18:23662\r\nConnection:keep-alive\r\nX-Client-project: project-152A-part2\r\n\r\n"
    clientSocket.send(request.encode())

    response = clientSocket.recv(4096)
    data = response.decode()
    # for debuggin purposes, look at header
    # print(response.decode())
    content_length = findContentLen(data)
    # print(content_length)
 
    # continue to grab pieces of data/packets from server
    while True:
        response = clientSocket.recv(4096)
        # append response data into an html file
        with open("ecs152a.html", "ab") as html_file:
            html_file.write(response)

        size += len(response)

        # break if reaches content-length
        if (size >= content_length):
            break

    numOfRequests = numOfRequests + 1
    # ----------FOR ABOVE THE FOLD PAGE LOAD TIME----------
    endTime_atf_plt = time.time()
    totalATF_PLT += (endTime_atf_plt - startTime_atf_plt)

# create images path if it does not exists
path_exists = os.path.isdir('images')
if not path_exists:
    os.mkdir('images')

# open html file and download images
with open("ecs152a.html") as f:
    content_length = 0
    size = 0

    # parse through html
    fileToParse = BeautifulSoup(f, "html.parser")
    # get all images
    for image in fileToParse.find_all("img"): 
        startTime_req = time.time()      

        # get image name/path
        img_str = "%(src)s"%image

        # print("Image Path: ", img_str)

        if (img_str[0] == 'i'):
            request = "GET /" + img_str + " HTTP/1.1\r\nHost: 173.230.149.18:23662\r\nConnection:keep-alive\r\nX-Client-project: project-152A-part2\r\n\r\n"
        else:
            continue
        
        if (x <= 3):
            # FOR ATF PLT
            startTime_atf_plt = time.time()
        # print("Sent request to server: ", request.encode())

        # reuse same TCP connection to send requests
        clientSocket.send(request.encode())

        response = clientSocket.recv(4096)  
        # print("Response from server: ", response)
        # response_header = response.split(b'\r\n\r\n')
        # print("Header: ",response_header[0])

        # Get the content-length
        cut_here = b'\r\n\r\n'
        if cut_here in response:
            temp1 = response.split(b'Content-length: ')
            temp2 = temp1[1].split(cut_here)
            content_length = int(temp2[0].decode())
            # print("Content Length: ", content_length)
            data_without_header = response.split(b'\r\n\r\n')
            img_binary = data_without_header[1]
            # print("Binary for Image: ", img_binary)
            with open(img_str, "ab") as f:
                f.write(img_binary)

            size += len(img_binary)
        # print(size)

        # continue to grab pieces of data/packets from server
        while True:
            # break if bigger than content size
            if (content_length != 0) and (size >= content_length):
                size = 0
                break

            response = clientSocket.recv(4096)
            # print("Response:", response)

            # create jpg files
            with open(img_str, "ab") as f:
                f.write(response)
            
            size += len(response)
            # print(size)
        
        numOfRequests = numOfRequests + 1
        # endTime_req = time.time()
        # ----------FOR ABOVE THE FOLD PAGE LOAD TIME----------
        if (x <= 3):
            endTime_atf_plt = time.time()
            totalATF_PLT += (endTime_atf_plt - startTime_atf_plt)
            x = x + 1

clientSocket.close()

endTime_plt = time.time()
# Calculations
PLT_time = endTime_plt - startTime_plt
avg_request_delay_time = PLT_time / numOfRequests
ATF_PLT_time = totalATF_PLT
rps_time = numOfRequests/PLT_time

print("************************************************")
print("HTTP Client Version: Persistent HTTP")
print("Total PLT = ", PLT_time)                         # get total page load time (PLT) of ecs152.html
print("Average Request Delay = ", avg_request_delay_time)   
print("ATF PLT = ", ATF_PLT_time)
print("RPS = ", round(rps_time,2))
print("************************************************")


# print("Number of Requests: ", numOfRequests)