from socket import *
import requests
import sys
import os
import webbrowser

port = sys.argv[1]
IP = '127.0.0.1'
serverport = int(port)
BASIC_URL_PART = "http://" + IP + ":" + port 

def Get_requests():
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n******  GET REQUEST FOR INDEX.HTML ******\n")
    res1 = requests.get(BASIC_URL_PART + "/index.html")
    print('HTTP/1.1 ' + str(res1.status_code) ,res1.reason,'\n', res1.headers, '\n\n', res1.text, '\n')
    print ("\n******  PREVIEW OF INDEX.HTML FILE WILL BE DISPLAYED ON BROWSER ******\n")
    webbrowser.get('firefox').open_new_tab(BASIC_URL_PART + "/index.html")
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("******  GET REQUEST FOR VIDEO.MP4 FILE ******\n")
    res2 = requests.get(BASIC_URL_PART + "/video.mp4")
    print('HTTP/1.1 ' + str(res2.status_code) ,res2.reason,'\n', res2.headers,'\n')
    print ("\n******  VIDEO WILL BE DISPLAY ON BROWSER ******\n")
    webbrowser.get('firefox').open_new_tab(BASIC_URL_PART + "/video.mp4")
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("******  GET REQUEST FOR IMAGE FILE ******\n")
    res3 = requests.get(BASIC_URL_PART + "/screenshot.png")
    print('HTTP/1.1 ' + str(res3.status_code) ,res3.reason,'\n', res3.headers,'\n')
    print ("\n******  IMAGE WILL BE DISPLAY ON BROWSER ******\n")
    webbrowser.get('firefox').open_new_tab(BASIC_URL_PART + "/screenshot.png")
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** checking If-Modified-Since Header ******")
    print ("****** GET /index.html with If-Modified-Since header ******")
    print('****** If-Modified-Since: Wed, 14 Nov 2021 14:28:00 GMT ******\n')
    res4 = requests.get(BASIC_URL_PART + "/index.html", headers={'If-Modified-Since': 'Sun, 14 Nov 2021 14:28:00 GMT'})
    print('HTTP/1.1 ' + str(res4.status_code) ,res4.reason,'\n', res4.headers, '\n\n', res4.text, '\n')
    print('file Not Modified ')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** checking If-Modified-Since Header ******")
    print ("****** GET /index.html with If-Modified-Since header ******")
    print('****** If-Modified-Since: Wed, 12 Nov 2021 14:28:00 GMT ******\n')
    res5 = requests.get(BASIC_URL_PART + "/index.html", headers={'If-Modified-Since': 'Fri, 12 Nov 2021 14:28:00 GMT'})
    print('HTTP/1.1 ' + str(res5.status_code) ,res5.reason,'\n', res5.headers, '\n\n', res5.text, '\n')
    print('file Modified')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** checking If-Unmodified-Since Header ******")
    print ("****** GET /index.html with If-Unmodified-Since header ******")
    print('****** If-Unmodified-Since: Wed, 12 Nov 2021 13:04:45 GMT ******\n')
    res6 = requests.get(BASIC_URL_PART + "/index.html", headers={'If-Unmodified-Since': 'Fri, 12 Nov 2021 13:04:45 GMT'})
    print('HTTP/1.1 ' + str(res6.status_code) ,res6.reason,'\n', res6.headers, '\n\n', res6.text, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** checking If-Unmodified-Since Header ******")
    print ("****** GET /index.html with If-Unmodified-Since header ******")
    print('****** If-Unmodified-Since: Sun, 14 Nov 2021 13:04:45 GMT ******\n')
    res7 = requests.get(BASIC_URL_PART + "/index.html", headers={'If-Unmodified-Since': 'Sun, 14 Nov 2021 13:04:45 GMT'})
    print('HTTP/1.1 ' + str(res7.status_code) ,res7.reason,'\n', res7.headers, '\n\n', res7.text, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** Range Header ******")
    print ("****** GET /index.html with partial range 5-50 ******\n")
    res8 = requests.get(BASIC_URL_PART + "/index.html", headers={'Range': 'bytes=5-50'})
    print('HTTP/1.1 ' + str(res8.status_code) ,res8.reason,'\n', res8.headers, '\n\n', res8.text, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** If-Range Header ******")
    print ("****** GET /index.html with partial range 50- ******\n")
    print('****** If-Range: Sun, 14 Nov 2021 13:04:45 GMT ******')
    res9 = requests.get(BASIC_URL_PART + "/index.html", headers={'If-Range': 'Sun, 14 Nov 2021 13:04:45 GMT','Range': 'bytes=50-'})
    print('HTTP/1.1 ' + str(res9.status_code) ,res9.reason,'\n', res9.headers, '\n\n', res9.text, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print("----- GET METHOD ------ ")
    print ("\n****** Unsupported Media ******")
    res10 = requests.get(BASIC_URL_PART + "/aniket.mrj")
    print('HTTP/1.1 ' + str(res10.status_code) ,res10.reason,'\n', res10.headers, '\n\n', res10.text, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print("----- GET METHOD ------ ")
    print ("\n****** URI TOO LONG ******")
    res10 = requests.get(BASIC_URL_PART + "/aniket.mrj")
    print('HTTP/1.1 ' + str(res10.status_code) ,res10.reason,'\n', res10.headers, '\n\n', res10.text, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")






def Post_requests():
    Post_Data1 = {  'name':'Aniket Warhade', 
                    'mobile':'7038700411', 
                    'age':22, 
                    'email':'abc@gmail.com', 
                    'gender':'Male',
                    }
    url = BASIC_URL_PART + "/post.html"
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** POSTING application/x-www-form-urlencoded TYPE DATA ******")
    print ("****** GET /POST.HTML CONTENT AFTER SUCCESSFULLY POSTING OF DATA ******\n")
    res1 = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=Post_Data1)
    print('HTTP/1.1 ' + str(res1.status_code) ,res1.reason,'\n', res1.headers, '\n\n', res1.text, '\n')
    print ("\n****** POST DATA ******\n")
    file_path = os.getcwd()+'/Post_files/x_www_form_urlencoded.txt'
    f=open(file_path,'r')
    print(f.read())
    f.close()
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** POSTING RAW_DATA DATA ******")
    print ("****** GET /POST.HTML CONTENT AFTER SUCCESSFULLY POSTING OF DATA ******\n")
    Post_Data2 = "The POST request is a fundamental method, and this method is mostly used when a user wants to send some sensitive data to the server like to send a form or some confidential data. "
    res2 = requests.post(url, headers={'Content-Type': 'text/plain'}, data=Post_Data2)
    print('HTTP/1.1 ' + str(res2.status_code) ,res2.reason,'\n', res2.headers, '\n\n', res2.text, '\n')
    print ("\n****** POST DATA ******\n")
    file_path = os.getcwd()+'/Post_files/raw_data.txt'
    f=open(file_path,'r')
    print(f.read())
    f.close()
    print("-------------------------------------------------------------------------------------------------------------------------------------------"









def Put_request():
    print ("\n****** PUTTING DATA ******")
    print ("****** CREATING NEW FILE  ******\n")
    url = BASIC_URL_PART + "/new.html"
    Put_Data = "PUT method is used to update resource available on the server. Typically, it replaces whatever exists at the target URL with something else. You can use it to make a new resource or overwrite an existing one. PUT requests that the enclosed entity must be stored under the supplied requested URI (Uniform Resource Identifier)"
    res1 = requests.put(url, data=Put_Data)
    print('hello')
    print('HTTP/1.1 ' + str(res1.status_code) ,res1.reason,'\n', res1.headers,'\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("****** LENGTH REQUIRED   ******\n")
    data = ""
    url = BASIC_URL_PART + "/new2.html"
    res2 = requests.put(url,  data=data)
    print('HTTP/1.1 ' + str(res2.status_code) ,res2.reason,'\n', res2.headers, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")




def Head_requests():
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n******  Head REQUEST FOR INDEX.HTML ******\n")
    res1 = requests.head(BASIC_URL_PART + "/index.html")
    print('HTTP/1.1 ' + str(res1.status_code) ,res1.reason,'\n', res1.headers, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** checking If-Modified-Since Header ******")
    print ("******  Head /index.html with If-Modified-Since header ******")
    print('****** If-Modified-Since: Wed, 14 Nov 2021 14:28:00 GMT ******\n')
    res2 = requests.head(BASIC_URL_PART + "/index.html", headers={'If-Modified-Since': 'Sun, 14 Nov 2021 14:28:00 GMT'})
    print('HTTP/1.1 ' + str(res2.status_code) ,res2.reason,'\n', res2.headers, '\n')
    print('file Not Modified ')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** checking If-Modified-Since Header ******")
    print ("****** Head /index.html with If-Modified-Since header ******")
    print('****** If-Modified-Since: Wed, 12 Nov 2021 14:28:00 GMT ******\n')
    res3 = requests.head(BASIC_URL_PART + "/index.html", headers={'If-Modified-Since': 'Fri, 12 Nov 2021 14:28:00 GMT'})
    print('HTTP/1.1 ' + str(res3.status_code) ,res3.reason,'\n', res3.headers, '\n')
    print('file Modified')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** checking If-Unmodified-Since Header ******")
    print ("****** HEAD /index.html with If-Unmodified-Since header ******")
    print('****** If-Unmodified-Since: Wed, 12 Nov 2021 13:04:45 GMT ******\n')
    res4 = requests.head(BASIC_URL_PART + "/index.html", headers={'If-Unmodified-Since': 'Fri, 12 Nov 2021 13:04:45 GMT'})
    print('HTTP/1.1 ' + str(res4.status_code) ,res4.reason,'\n', res4.headers, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print ("\n****** checking If-Unmodified-Since Header ******")
    print ("****** HEAD /index.html with If-Unmodified-Since header ******")
    print('****** If-Unmodified-Since: Sun, 14 Nov 2021 13:04:45 GMT ******\n')
    res5 = requests.head(BASIC_URL_PART + "/index.html", headers={'If-Unmodified-Since': 'Sun, 14 Nov 2021 13:04:45 GMT'})
    print('HTTP/1.1 ' + str(res5.status_code) ,res5.reason,'\n', res5.headers, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print("----- HEAD Method ------ ")
    print ("\n****** Unsupported Media ******")
    res6 = requests.head(BASIC_URL_PART + "/aniket.mrj")
    print('HTTP/1.1 ' + str(res6.status_code) ,res6.reason,'\n', res6.headers, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")
    print("----- HEAD Method ------ ")
    print ("\n****** URI TO LONG ******")
    res7 = requests.head(BASIC_URL_PART + "/abcdefghijklmnopqrstuvwxyz/abcdef")
    print('HTTP/1.1 ' + str(res7.status_code) ,res7.reason,'\n', res7.headers, '\n')
    print("-------------------------------------------------------------------------------------------------------------------------------------------")


def version_not_supported():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((IP,serverport))
    request = "HEAD /index.html HTTP/2.1"
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024)
    print(response.decode())
    print('---------------------------------------------------------------------HEAD /index.html HTTP/2.1-----------------------------------------------------------------------\n\n',response.decode())
    clientSocket.close()

def main():
    print("***************************************************** -- GET METHOD --*********************************************************************")
    Get_requests()
    print("***************************************************** -- HEAD METHOD --********************************************************************")
    Head_requests()
    print("***************************************************** -- POST METHOD --********************************************************************")
    Post_requests()
    version_not_supported()
    #Put_request()
    


if __name__ == "__main__":
    main()

