from socket import *
import threading
import sys


serverName = '127.0.0.1'
serverPort = int(sys.argv[1])


def get_request():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    request = "GET / HTTP/1.1"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024)
    print('---GET /index.html HTTP/1.1---\n\n',response.decode())
    clientSocket.close()


def head_request():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    request = "HEAD /index.html HTTP/1.1"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024)
    print('---HEAD /index.html HTTP/1.1---\n\n',response.decode())
    clientSocket.close()

def delete_request():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    request = "DELETE /new7.html HTTP/1.1\r\nHost: 127.0.0.1:1234\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36\r\nCache-Control: no-cache\r\nAuthorization: Basic VkFNSzp2YW1rMTQxMA==\r\nPostman-Token: 87b2ab5a-38d9-0248-430f-34efb3e0a7f0\r\nAccept: */*\r\nOrigin: chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: cors\r\nSec-Fetch-Dest: empty\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\n\r\n"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024)
    print('---DELETE /new7.html HTTP/1.1---\n\n',response.decode())
    clientSocket.close()



def length_required():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    request = "PUT /new8.html HTTP/1.1\r\nHost: 127.0.0.1:1234\r\nConnection: keep-alive\r\nAuthorization: Basic VkFNSzp2YW1rMTQxMA==\r\nPostman-Token: 0d50bc71-239b-7c7f-31d7-c246a410e788\r\nCache-Control: no-cache\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36\r\nContent-Type: text/plain;charset=UTF-8\r\nAccept: */*\r\nOrigin: chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: cors\r\nSec-Fetch-Dest: empty\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\n\r\nHello"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024)
    print('---PUT /new8.html HTTP/1.1 without content length---\n\n',response.decode())
    clientSocket.close()

def method_not_implemented():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    request = "GETT /index.html HTTP/1.1"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024)
    print('---GETT /index.html HTTP/1.1---\n\n',response.decode())
    clientSocket.close()

def file_put_request():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    request = "PUT /new9.html HTTP/1.1\r\nHost: 127.0.0.1:1234\r\nConnection: keep-alive\r\nContent-Length: 271\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36\r\nCache-Control: no-cache\r\nAuthorization: Basic VkFNSzp2YW1rMTQxMA==\r\nPostman-Token: bd79ce4d-dd00-9deb-ccc4-974ee9d8f405\r\nAccept: */*\r\nOrigin: chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: cors\r\nSec-Fetch-Dest: empty\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\n\r\n<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">\r\n<html>\r\n<head>\r\n<title>200 Ok</title>\r\n</head>\r\n<body>\r\n<h1>Ok</h1>\r\n<h4>The file was already present. The content is modified.</h4>\r\n<hr>\r\n<address>Apache/2.4.41 (Ubuntu) Server at 127.0.0.1</address>\r\n</body>\r\n</html>"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024)
    print('---PUT /new9.html HTTP/1.1 file data---\n\n',response.decode())
    clientSocket.close()

def simple_put_request():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    request = "PUT /new8.html HTTP/1.1\r\nHost: 127.0.0.1:1234\r\nConnection: keep-alive\r\nContent-Length: 5\r\nAuthorization: Basic VkFNSzp2YW1rMTQxMA==\r\nPostman-Token: 0d50bc71-239b-7c7f-31d7-c246a410e788\r\nCache-Control: no-cache\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36\r\nContent-Type: text/plain;charset=UTF-8\r\nAccept: */*\r\nOrigin: chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: cors\r\nSec-Fetch-Dest: empty\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\n\r\nHello"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024)
    print('---PUT /new8.html HTTP/1.1---\n\n',response.decode())
    clientSocket.close()

def unsupported_media_type():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    request = "GET /demo.pptx HTTP/1.1"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024)
    print('---GET /demo.pptx HTTP/1.1---\n\n',response.decode())
    clientSocket.close()

def main():
    get_request()
    head_request()
    simple_put_request()
    file_put_request()
    method_not_implemented()
    unsupported_media_type()
    length_required()



if __name__ == "__main__":
    main()
