from socket import *
from threading import *
import sys
import os
import time
import datetime

content_type = {
        'html':'text/html', 'txt':'text/plain', 'png':'image/png', 'gif': 'image/gif', 'jpg':'image/jpg',
        'ico': 'image/x-icon', 'php':'application/x-www-form-urlencoded', '': 'text/plain', 'jpeg':'image/jpeg',
        'pdf': 'application/pdf', 'js': 'application/javascript', 'css': 'text/css', 'mp3' : 'audio/mpeg',
        'mp4': 'video/mp4'
        }

status_codes = {
        200:'OK', 201: 'Created', 204: 'No Content', 301: 'Moved Permanently',304: 'Not Modified', 
        400:'Bad Request', 401: 'Unauthorized', 403: 'Forbidden', 404:'Not Found', 408: 'Request Timeout',
        411: 'Length Required', 413: 'Payload Too Large', 414: 'URI Too Long', 
        415: 'Unsupported Media Type', 500: 'Internal Server Error', 501:'Not Implemented',
        503: 'Service Unavailable',     505:'HTTP Version not Supported'
        }

mode = {
        'html':'r', 'txt':'r', 'png':'rb', 'gif': 'rb', 'jpg':'rb',
        'ico': 'rb', 'php':'r', '': 'r', 'jpeg':'rb', 'pdf': 'r',
        'js': 'r', 'css': 'r', 'mp3' : 'rb', 'mp4': 'rb'
        }



'''{'method': 'GET', 'uri': '/', 'version': 'HTTP/1.1', 'Host': '127.0.0.1', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Linux"', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9,mr;q=0.8'}
'''

def parse_Http_Request(req):      # parse/handle the http request made by client
    reqlines = req.split("\r\n")
    start_line = reqlines[0].split()
    req = {}
    if (len(start_line))>0:
        method = start_line[0]
    req['method'] = method
    if (len(start_line)>1):
       req['uri'] = start_line[1]
    if (len(start_line)>2):
        req['version'] = start_line[2]

    if len(reqlines)>1:
        for line in reqlines[1:-2]:
            header = line.split(":")
            req[header[0]] = header[1][1:]
        if (method=='POST' or method=='PULL'):
            req['body']=reqlines[-1]

    return req


# convert date from this form  Sun Oct 17 21:07:53 2021     to this form    Sun, 17 Oct 2021 21:07:53 GMT
def new_date_format(s):
        form = s.split(' ')
        date = f"{form[0]}, {form[2]} {form[1]} {form[4]} {form[3]} GMT"
        return date


def get_statusCode_Headers(req,status_code,fileName):
    res = ""
    res += f"{req['version']} {status_code} {status_codes[status_code]}\n"
    res += "Date: "+ str(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")) + "\n"
    res += "Server: Apache/2.4.18 (Ubuntu)\n"
    f = open(fileName,"r")
    file_content= f.read()
    res += "Content-Type: text/html\n"
    res += "Content-Length: " + str(len(file_content)) + "\n"
    res += "Connection: Closed\n\n"
    if req['method'] == 'GET':
        res += file_content 
    return res





def getOrHead_method(req):
    global res
    try:
        if req['uri']=='/':
            req['uri'] = "/index.html"
        PATH = os.getcwd()
        PATH += req['uri']
        if os.path.isfile(PATH) :   #checking file exist or not                         
            if os.access(PATH,os.R_OK) :  # checking permission of file i.e accesible for reading or not
                status_code = 200
                fileName = req['uri'].strip('/')
                split_file_name = fileName.split('.')
                ext = split_file_name[1]
                if content_type.get(ext) == None :
                    status_code = 415
                    fileName = '415_unsupported_media.html'
                    res = get_statusCode_Headers(req,status_code,fileName)
                    return res
                else:
                    res = f"{req['version']} {status_code} {status_codes[status_code]}\n"
                    res +="Date: "
                    date_time = str(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")) + "\n"
                    res += date_time
                    res += "Server: "
                    res += "Apache/2.4.18 (Ubuntu)"
                    res += "\r\nLast_Modified: "
                    modification_time = time.ctime(os.path.getmtime(fileName))
                    last_modified = new_date_format(modification_time)
                    res += last_modified
                    f = open(fileName, mode[ext])
                    text = f.read() 
                    res += "\n"
                    res += "Accept-Ranges: bytes"
                    if req.get('Accept-Language') != None :
                        res += "\nContent-Language: "
                        res += req['Accept-Language']
                    if mode.get(ext) != None :
                        cont_type = content_type[ext]
                        res += "\nContent-Type: "
                        res += cont_type
                    res += "\nContent-Length: "
                    res += str(len(text))
                    res += "\nConnection: keep-alive"
                    res += "\n\n"
                    if req['method'] == 'GET':
                        res += text
                    print(res)
                    return res
            else:
                status_code = 403
                #res =  f"{req['version']} {status_code} {status_codes[status_code]}\n\n"
                #res+= "<h1> Forbidden file </h1>"
                fileName = '403_forbidden.html'
                res = get_statusCode_Headers(req,status_code,fileName)
                return res
        else:
            status_code = 404
            #res =  f"{req['version']} {status_code} {status_codes[status_code]}\n\n"
            #res+= "<h1> Not found </h1>"
            fileName = 'Not_found.html'
            res = get_statusCode_Headers(req,status_code,fileName)
            return res
    except:
        status_code = 400
        #res =  f"{req['version']} {status_code} {status_codes[status_code]}\n\n"
        #res+=  "<h1> Bad Request </h1>"
        fileName = '400_Bad_request.html'
        res = get_statusCode_Headers(req,status_code,fileName)
        return res
                


    

    
def httpResponse(req):
    if req['version'] == 'HTTP/1.1':
        method = req['method']
        if (method == 'GET' or method == 'HEAD') :
            res=getOrHead_method(req)
        elif method == 'POST':
            pass
        elif method == 'PUT':
            pass
        elif method == 'DELETE':
            pass
    elif req['version'][0:5] == 'HTTP/':
        status_code = 505 
        #res =  f"{req['version']} {status_code} {status_codes[status_code]}\n\n"
        #res+=  "<h1> Http version Not supported! </h1>"
        fileName = '505_version.html'
        res = get_statusCode_Headers(req,status_code,fileName)

    else:
        status_code = 400
        #res =  f"{req['version']} {status_code} {status_codes[status_code]}\n\n"
        #res+=  "<h1> Bad Request </h1>"
        fileName = '400_Bad_request.html'
        res = get_statusCode_Headers(req,status_code,fileName)
   
        



def main():

    serverPort = int(sys.argv[1])

    serverSocket = socket(AF_INET, SOCK_STREAM)

    serverSocket.bind(("",serverPort))

    serverSocket.listen(5)
    print("server is ready to listen on port: ",serverPort)

    while True:
        connection,clientAddress = serverSocket.accept()
        print("Connection Succesful at  :",clientAddress)
        data = connection.recv(1024)
        req = data.decode()
        req2 = parse_Http_Request(req)
        print(req2)
        t1 = Thread(target = httpResponse, args = (req2, ))
        t1.start()
        time.sleep(0.001)
        connection.send(res.encode())
        connection.close()

if __name__=="__main__":
    main()
