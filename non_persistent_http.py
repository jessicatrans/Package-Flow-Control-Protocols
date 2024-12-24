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
# startTime_req = 0
# endTime_req = 0

ATF_PLT_time = 0
startTime_atf_plt = 0
endTime_atf_plt = 0
totalATF_PLT = 0
x = 0

rps_time = 0

numOfRequests = 0
# req_to_res_time = 0
# totalReqDelay = 0
# requestDelayList = []


startTime_plt = time.time()         
# check if ecs152a.html file exists, if not then create html file
file_exists = os.path.exists('ecs152a.html')
if not file_exists: # if false, get esc152.html file from server
    size = 0
    content_length = 0

    # FOR ATF PLT
    startTime_atf_plt = time.time()

    # create TCP socket object, IPv4
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # client sends to server, connection must be established --> three way handshake
    clientSocket.connect((host, port))
    request = "GET /ecs152a.html HTTP/1.1\r\nHost: 173.230.149.18\r\nConnection:close\r\nX-Client-project: project-152A-part2\r\n\r\n"
    clientSocket.send(request.encode())

    # FOR AVERAGE REQUEST DELAY
    # startTime_req = time.time()     # start time since making request    

    response = clientSocket.recv(4096)
    data = response.decode()

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

    clientSocket.close()

    # ----------FOR AVERAGE RELAY DELAY----------
    # endTime_req = time.time()       # end time after receiving last socket
    # # update request delay sum
    # req_to_res_time = endTime_req - startTime_req
    # totalReqDelay += req_to_res_time 
    # keep track of how many requests are being sent
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
        # get image name/path
        img_str = "%(src)s"%image

        # print("Image Path: ", img_str)

        if (img_str[0] == 'i'):
            request = "GET /" + img_str + " HTTP/1.1\r\nHost: 173.230.149.18\r\nConnection:close\r\nX-Client-project: project-152A-part2\r\n\r\n"
        else:
            continue

        if (x <= 3):
            # FOR ATF PLT
            startTime_atf_plt = time.time()

        # create TCP socket object
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # open another TCP connection for get images
        clientSocket.connect((host, port))
        clientSocket.send(request.encode())

        # startTime_req = time.time()                     # start time since making request    

        response = clientSocket.recv(4096)        
        data = response.decode()

        # Get the content-length
        content_length = findContentLen(data)

        # continue to grab pieces of data/packets from server
        while True:
            response = clientSocket.recv(4096)

            # create jpg files
            with open(img_str, "ab") as f:
                f.write(response)
            
            size += len(response)

            # break if bigger than content size
            if (size >= content_length):
                size = 0
                break
        
        clientSocket.close()
        # ----------FOR AVERAGE RELAY DELAY----------
        # endTime_req = time.time()                       # end time after receiving last socket
        # req_to_res_time = endTime_req - startTime_req
        # totalReqDelay += req_to_res_time                # get sum of request delay in order to calculate average request delay
        numOfRequests = numOfRequests + 1               # increment number of requests made

        # ----------FOR ABOVE THE FOLD PAGE LOAD TIME----------
        if (x <= 3):
            endTime_atf_plt = time.time()
            totalATF_PLT += (endTime_atf_plt - startTime_atf_plt)
            x = x + 1

endTime_plt = time.time()

# Calculations 
PLT_time = endTime_plt - startTime_plt
avg_request_delay_time = PLT_time / numOfRequests
ATF_PLT_time = totalATF_PLT
rps_time = numOfRequests/PLT_time

print("************************************************")
print("HTTP Client Version: Non-Persistent HTTP")
print("Total PLT = ", PLT_time)                         # get total page load time (PLT) of ecs152.html
print("Average Request Delay = ", avg_request_delay_time)   
print("ATF PLT = ", ATF_PLT_time)
print("RPS = ", round(rps_time,2)) 
print("************************************************")


# print("Number of Requests: ", numOfRequests)