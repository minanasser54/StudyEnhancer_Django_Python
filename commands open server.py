import os
import webbrowser
import socket
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)
webbrowser.open("http://{}:8000".format(IPAddr))
os.system('cmd /k "cd scripts & activate & cd.. & cd src & pyhton manage.py runserver {}:8000"'.format(IPAddr))
