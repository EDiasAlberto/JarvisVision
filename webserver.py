from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, jarvis, **kwargs):
        # Initialize custom attributes
        self.jarvis = jarvis
        # Call the parent class's __init__
        super().__init__(*args, **kwargs)

    def do_GET(self):
        
        # Respond to the request
        self.send_response(200)  # HTTP status code 200 (OK)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Function executed successfully!")
        self.jarvis.mainLoop() 


# Run the server
if __name__ == "__main__":
    run_server()
