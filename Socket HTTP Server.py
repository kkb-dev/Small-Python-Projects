import socket # Use TCP/IP
import os # Interact with Windows File System
import mimetypes # Infer about what file type something is
# Kevan Basnayake - CSCI 379 Computer Networking - Programming Assignment

# Choose hostname and port number to bind to
HOST,PORT = '0.0.0.0',8000

# Choose a custom directory to get files from (r'C:\Users\')
# Choose ('') to get directory the python file sits in
DIRS_1 = ''

# Ignore requests cached by web browser
IGNORE = ["/favicon.ico"]

# -----------------------------------------------------------
# Create and bind socket (TCP)
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
# Only one connection accepted
my_socket.listen(1)

print('SERVER IS RUNNING:',HOST,PORT)
while True:
    connection,address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    string_list = request.split(' ')
    
    # Get the client's current URL
    try:
        if string_list[1] not in IGNORE:
            url = string_list[1]
            print("URL:",url)
    except:
        pass

    try:
        # If DIRS is empty, get current directory
        DIRS = DIRS_1
        if len(DIRS_1) == 0:
            DIRS_1 = os.path.dirname(os.path.realpath(__file__))
            
        # Get current directory based on URL
        if url != "/":
            DIRS += url.replace("/","\\")
            DIRS = DIRS.replace("%20",' ')
            
        # Create html template for http response
        header = 'HTTP/1.1 200 OK\n'
        response_head = ("""
        <html>
        <body>
        <h3>Kevan Basnayake CSCI 379 - HTTP Server</h3>
        <p>Here is list of all available directories to be served.</p>
        <hr>
        <p>Current Directory: %s<p>
        <hr>""" % (DIRS))

        # If non-directory, serve file
        if not os.path.isdir(DIRS) and "." in DIRS:
            # Read file in bytes and send as reponse
            file = open(DIRS,'rb')
            response = file.read()
            file.close()
            # Create header for reponse and attach type
            header = 'HTTP/1.1 200 OK\n'
            # Guess file type, or resort to text            
            mimetype = mimetypes.guess_type(DIRS)[0] or 'text/html'
            print("Serving",mimetype)
            header += 'Content-Type: '+str(mimetype)+'\n\n'

        # If directory, 
        else:
            response_body = ''
            # List all files/directories in current directory  
            for o in (os.listdir(DIRS)):
                # Loop through list and create a link for each object
                dirlink = (url + "/" + o).replace("//","/")
                if os.path.isdir(DIRS) and "." not in o:
                    o = o + " \\"
                link = '<a href="%s">%s</a><br>' % (dirlink,o)
                response_body += link

            # Create end of html body
            response_tail = ("""
            </body>
            </html>""")

            # Compose html template
            response = (response_head + response_body + response_tail).encode('utf-8')

    # Create 404 Error for invalid requests      
    except Exception as e:
        print("Error",e)
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = ''.encode('utf-8')

    # Send response and close
    finally:
        final_response = header.encode('utf-8')
        final_response += response
        connection.send(final_response)
        connection.close()
