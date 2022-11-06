#!/bin/env python3
"""
A web server that serves audio files from the current directory.
Listens on port 8080 and provides a simple web interface for users to browse and play audio files.
"""
import os
import http.server
import socketserver
from urllib.parse import urlparse, unquote
import mimetypes

# Define the port to listen on
PORT = 8080

# HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Audio Player</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        li {{
            margin: 10px 0;
            padding: 10px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        audio {{
            width: 100%;
            margin-top: 10px;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>Audio Files</h1>
    <ul>
        {audio_list}
    </ul>
</body>
</html>
"""

class AudioHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_url = urlparse(self.path)
        path = unquote(parsed_url.path)
        
        # Serve the root directory with a list of audio files
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Get all audio files in the current directory
            audio_files = []
            for file in os.listdir('.'):
                if os.path.isfile(file) and self.is_audio_file(file):
                    audio_files.append(file)
            
            # Generate HTML list items for each audio file
            audio_list_html = ""
            for file in audio_files:
                audio_list_html += f"""
                <li>
                    <a href="/{file}">{file}</a>
                    <audio controls>
                        <source src="/{file}" type="{self.get_mime_type(file)}">
                        Your browser does not support the audio element.
                    </audio>
                </li>
                """
            
            # Fill the template with the audio list
            html_content = HTML_TEMPLATE.format(audio_list=audio_list_html)
            self.wfile.write(html_content.encode())
        else:
            # Serve the requested file
            super().do_GET()
    
    def is_audio_file(self, filename):
        """Check if a file is an audio file based on its extension."""
        audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a']
        return any(filename.lower().endswith(ext) for ext in audio_extensions)
    
    def get_mime_type(self, filename):
        """Get the MIME type for a file."""
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type or 'application/octet-stream'

def get_host_addresses():
    import socket
    hostname = socket.gethostname()
    ip_addresses = []
    
    # Get all IP addresses for the machine
    try:
        # Get the primary IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addresses.append(s.getsockname()[0])
        s.close()
    except:
        pass
        
    # Get all network interface addresses
    try:
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if ip not in ip_addresses and not ip.startswith("127."):
                ip_addresses.append(ip)
    except:
        pass
        
    # Add localhost
    if "127.0.0.1" not in ip_addresses:
        ip_addresses.append("127.0.0.1")
    
    return hostname, ip_addresses

def main():
    # Initialize MIME types
    mimetypes.init()
    
    # Create the server
    handler = AudioHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        # Get all network interfaces
        hostname, ip_addresses = get_host_addresses()
            
        # Print all available URLs
        print("Server available at:")
        for ip in ip_addresses:
            print(f"  http://{ip}:{PORT}")
        print(f"  http://{hostname}:{PORT}")
        print(f"Serving at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    main()
