from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import os

# Example of a valid POST request
#curl -X POST -H "Content-Type: application/json" -H "Authorization: <secure_token>" -d '{"deploy": "test_deploy"}' http://localhost:5001/

# Go to the directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current directory to the script directory
os.chdir(current_dir)

# Define the authentication token
auth_token = "<secure_token>"

# Define the deploy command
deploy_command = "./deploy.sh"

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Verify if the request contains the Authorization header
        if self.headers.get("Authorization") != auth_token:
            self.send_error(401, "Unauthorized")
            return

        # Verify if the request contains the Content-Type header
        content_length = int(self.headers.get("Content-Length"))
        body = self.rfile.read(content_length).decode("utf-8")

        # Convert the body to a dictionary
        data = json.loads(body)

        # Verify if the request contains the deploy key
        if "deploy" not in data:
            self.send_error(400, "Bad Request")
            return

        # Get the deploy name
        deploy_name = data.get("deploy")

        # Run the deploy command
        try:
            print(f"Executing deploy {deploy_name}")

            process = subprocess.Popen(deploy_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            for line in iter(process.stdout.readline, b''):
                self.wfile.write(line)
            process.wait()
            self.wfile.flush()
        except subprocess.CalledProcessError as e:
            self.send_error(500, f"Internal Server Error: {e}")
            return

if __name__ == "__main__":
    server_address = ("", 5001)
    print(f"Starting server on port {server_address[1]}")
    print(f"Wating for POST requests on localhost:{server_address[1]}")
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()