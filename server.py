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
        200:'OK', 201: 'Created', 204: 'No Content', 206: 'Partial Content', 301: 'Moved Permanently',304: 'Not Modified', 
        400:'Bad Request', 401: 'Unauthorized', 403: 'Forbidden', 404:'Not Found', 408: 'Request Timeout',
        411: 'Length Required', 413: 'Payload Too Large', 414: 'URI Too Long', 
        415: 'Unsupported Media Type', 500: 'Internal Server Error', 501:'Not Implemented',
        503: 'Service Unavailable',     505:'HTTP Version not Supported'
        }



def parse_Http_Request(request):      # parse/handle the http request made by client
    reqlines = request.split("\r\n")
    req = {}

    start_line = reqlines[0].split()
    if (len(start_line))>0:
        method = start_line[0]
        req['method'] = method
    if (len(start_line)>1):
       req['uri'] = start_line[1]
    if (len(start_line)>2):
        req['version'] = start_line[2]

    for line in reqlines:
        if "If-Modified-Since" in line :
            If_Modified = line
            reqlines.remove(line)
            If_Modified = If_Modified.split(":",1)
            req[If_Modified[0]] = If_Modified[1][1:]
            break

    if len(reqlines)>1:
        for line in reqlines[1:-2]:
            header = line.split(":")
            req[header[0]] = header[1][1:]
        if (method=='POST' or method=='PULL'):
            req['body']=reqlines[-1]

    return req


# convert date from this form  Sun Oct 17 21:07:53 2021     to this form    Sun, 17 Oct 2021 21:07:53 GMT
def Handle_date_format(s):
        form = s.split(' ')
        date = f"{form[0]}, {form[2]} {form[1]} {form[4]} {form[3]} GMT"
        return date


def get_statusCode_Headers(req,status_code,fileName):
    res = ""
    res += f"{req['version']} {status_code} {status_codes[status_code]}\n"
    res += "Date: "+ str(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")) + "\n"
    res += "Server: Apache/2.4.18 (Ubuntu)\n"
    f = open(fileName,"rb")
    file_content= f.read()
    res += "Content-Type: text/html\n"
    res += "Content-Length: " + str(len(file_content)) + "\n"
    res += "Connection: Closed\n\n"
    res = res.encode()
    if req['method'] != 'HEAD':
        res += file_content 
    return res




def Handle_range_Header(f,rangeList):
    data = b''
    for byteRange in rangeList:
        byteRange = byteRange.split("-")
        if byteRange[0].strip() == "" :
            f.seek(0)
            n=int(byteRange[1].strip())
            data += f.read(n)
        elif byteRange[1] == "" :
            f.seek(int(byteRange[0].strip()))
            data += f.read()
        else:
            f.seek(int(byteRange[0]))
            n = int(byteRange[1].strip())-int(byteRange[0].strip())
            data += f.read(n+1)

    return data

def Handle_If_Modified_Since(req,fileName):
    If_Modified = req['If-Modified-Since']
    date_time = datetime.datetime.strptime(If_Modified,"%a, %d %b %Y %H:%M:%S GMT")
    prev_req_time_in_sec = int(time.mktime(date_time.timetuple()))  #get No of  second passed since epoch 
    file_modified_time_in_sec = int(os.path.getmtime(fileName))
    if(prev_req_time_in_sec < file_modified_time_in_sec):
            status_code = 200
    else:
            status_code = 304
    return status_code

    

def getOrHead_method(req):
    res= ""
    try:
        if req['uri']=='/':
            req['uri'] = "/index.html"
        PATH = os.getcwd()
        PATH += req['uri']
        if os.path.isfile(PATH) :   #checking file exist or not                         
            if os.access(PATH,os.R_OK) :  # checking permission of file i.e accesible for reading or not
                status_code = 200
                fileName = req['uri'].strip('/')
                #print(fileName)
                split_file_name = fileName.split('.')
                ext = split_file_name[1]
                #print(ext)
                if content_type.get(ext) == None :
                    status_code = 415
                    fileName = '415_unsupported_media.html'
                    res = get_statusCode_Headers(req,status_code,fileName)
                    return res
                else:
                    status_code = 200
                    body =  b''
                    f = open(fileName, "rb")
                    if req.get('If-Modified-Since')!=None:
                        status_code = Handle_If_Modified_Since(req,fileName)
                    if req.get('Range') != None :
                        status_code = 206
                    #  handle resoponse body according to status code .
                    if (status_code == 200 ):
                        body += f.read()
                    elif (status_code == 206 ) :
                        byteRange = req['Range'][6:]
                        byteRange = byteRange.split(", ")
                        #print(byteRange)
                        body += Handle_range_Header(f,byteRange)
                    elif (status_code == 304 ):
                        body = b''

                    res += f"{req['version']} {status_code} {status_codes[status_code]}"  # status line
                    res +="\nDate: "
                    date_time = str(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))
                    res += date_time
                    res += "\nServer: "
                    res += "Apache/2.4.18 (Ubuntu)"
                    res += "\nLast_Modified: "
                    modification_time = time.ctime(os.path.getmtime(fileName))
                    last_modified = Handle_date_format(modification_time)
                    res += last_modified 
                    res += "\nAccept-Ranges: bytes"
                    if req.get('Accept-Language') != None :
                        res += "\nContent-Language: "
                        res += req['Accept-Language']
                    else:
                        res += "\nContent-Language: en-US,en;q=0.9"

                    if content_type.get(ext) != None :
                        cont_type = content_type[ext]
                        res += "\nContent-Type: "
                        res += cont_type
                    res += "\nContent-Length: "
                    res += str(len(body))
                    res += "\nConnection: keep-alive"
                    res += "\n\n"
                    res = res.encode()
                    if req['method']=='GET' :
                        res += body
                    return res;

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
                


def delete_method(req):
    res = ""
    if req['uri']=='/':
        req['uri'] = "/index.html"
    PATH = os.getcwd()
    PATH += req['uri']
    if os.path.isfile(PATH) :   #checking file exist or not
        if (os.access(PATH,os.R_OK) and os.access(PATH, os.W_OK) ) :
            fileName = req['uri'].strip('/')
            f = open(fileName,"rb")
            body = b''
            body += f.read()
            file_length = len(body)
            if len(body)==0:
                status_code = 204
                res += f"{req['version']} {status_code} {status_codes[status_code]}"
                res += "\n\n"
                os.remove(fileName)
                res = res.encode()
                return res
            else:
                status_code = 200
                res += f"{req['version']} {status_code} {status_codes[status_code]}"
                res +="\nDate: "
                date_time = str(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))
                res += date_time
                os.remove(fileName)
                res+= "\n\n"
                res+= "<h1>File Deleted!</h1>\n"
                res = res.encode()
                return res
        else:
            status_code = 403
            fileName = '403_forbidden.html'
            res = get_statusCode_Headers(req,status_code,fileName)
            return res
    else:
        status_code = 400
        fileName = '400_Bad_request.html'
        res = get_statusCode_Headers(req,status_code,fileName)
        return res

    
def httpResponse(connection,req):
    if req['version'] == 'HTTP/1.1':
        method = req.get('method')
        if (method == 'GET' or method == 'HEAD') :
            res = getOrHead_method(req)
            connection.send(res)
            connection.close()
        elif method == 'POST':
            pass
        elif method == 'PUT':
            pass
        elif method == 'DELETE':
            res = delete_method(req)
            connection.send(res)
            connection.close()
    elif req['version'][0:5] == 'HTTP/':
        status_code = 505 
        #res =  f"{req['version']} {status_code} {status_codes[status_code]}\n\n"
        #res+=  "<h1> Http version Not supported! </h1>"
        fileName = '505_version.html'
        res = get_statusCode_Headers(req,status_code,fileName)
        connection.send(res)
        connection.close()

    else:
        status_code = 400
        #res =  f"{req['version']} {status_code} {status_codes[status_code]}\n\n"
        #res+=  "<h1> Bad Request </h1>"
        fileName = '400_Bad_request.html'
        res = get_statusCode_Headers(req,status_code,fileName)
        connection.send(res)
        connection.close()
   


def quitServer(serverSocket):
    while True:
        cmd = input()
        cmd = cmd.lower()
        if (cmd == 'stop'):
            print("Server stopped")
            serverSocket.close()
            os._exit(os.EX_OK)
            break



def main():

    serverPort = int(sys.argv[1])

    serverSocket = socket(AF_INET, SOCK_STREAM)

    serverSocket.bind(("",serverPort))

    serverSocket.listen(5)
    print(f'The server is ready to receive on http://127.0.0.1:{serverPort}')
    
    quit_thread = Thread(target = quitServer, args = (serverSocket,))
    quit_thread.start()

    while True:
        connection,clientAddress = serverSocket.accept()
        print("Connection Succesful at  :",clientAddress)
        data = connection.recv(1024)
        req = data.decode()
        req2 = parse_Http_Request(req)
        #print(req2)
        t1 = Thread(target = httpResponse, args = (connection,req2,))
        t1.start()

if __name__=="__main__":
    main()





