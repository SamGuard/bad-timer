import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from os import environ





def main():
    global outputString
    now = datetime.datetime.today()
    #end = datetime.datetime(2021, 4, 9, 19, 59, 45)
    end = datetime.datetime(2023, 5, 30, 23, 59, 59)


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
            self.wfile.write(bytes("<html><head><title>BAD TIMER</title></head>", "utf-8"))
            self.wfile.write(bytes("""
                <link rel="preconnect" href="https://fonts.gstatic.com">
                <link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@700&display=swap" rel="stylesheet"> 
            """, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("""<p id='num' style='font-family: "Roboto Condensed", "sans-serif"; font-size: 256px; color: white;'></p>""", "utf-8"))
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



if __name__ == '__main__':
    print("starting server")
    hostName = "0.0.0.0"
    serverPort = int(environ.get('PORT', 5000)) 
    outputString = "24:00:00"  
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
