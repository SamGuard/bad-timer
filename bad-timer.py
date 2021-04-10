import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from os import environ

hostName = "localhost"
try:
    serverPort = int(environ['PORT'])
except:
    serverPort = 3000
print(serverPort)
outputString = "24:00:00"


def main():
    global outputString
    now = datetime.datetime.today()
    #end = datetime.datetime(2021, 4, 9, 19, 59, 45)
    end = datetime.datetime(2021, 4, 10, 12, 0, 0)


    diff = diff = (end - now)

    while now <= end:
        now = datetime.datetime.today()
        diffNew = (end - now)
        if (diffNew is not diff):
            timeLeft = diff.total_seconds()
            diff = diffNew
            hours = int(timeLeft // (60*60))
            minutes = int((timeLeft - hours * 60 * 60) // (60))
            seconds = int((timeLeft - hours * 60 * 60 - minutes * 60))
            
            hours = str(hours)
            if(len(hours) < 2):
                hours = "0"+hours

            minutes = str(minutes)
            if(len(minutes) < 2):
                minutes = "0"+minutes
                
            seconds = str(seconds)
            if(len(seconds) < 2):
                seconds = "0"+seconds
            

            s = hours + ":" + minutes + ":" + seconds
            #print(s)
            outputString = s



class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global outputString
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if(self.path == "/"):
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("""<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet"/>""", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("""<p id='num' style="font-family: 'Roboto', sans-serif"; 15px'></p>""", "utf-8"))
            self.wfile.write(bytes("""
            <script>
                function update(){
                var xmlHttp = new XMLHttpRequest();
                xmlHttp.open( "GET", "/num", false ); // false for synchronous request
                xmlHttp.send( null );
                document.getElementById("num").innerHTML = xmlHttp.responseText;
                }
                setInterval(update, 200)
            </script>
            """, "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        else:
            self.wfile.write(bytes(outputString, "utf-8"))

    def log_message(self, format, *args):
        return



          
timer = threading.Thread(target=main, daemon=True)
timer.start() 
webServer = HTTPServer((hostName, serverPort), MyServer)
print("Server started http://%s:%s" % (hostName, serverPort))

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
print("Server stopped.")
