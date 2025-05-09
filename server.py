from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Replace this with your actual backend server
BACKEND_SERVER = "http://50.47.224.9:5000"

@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def proxy(path):
    backend_url = f"{BACKEND_SERVER}/{path}"
    
    # Forward headers except Host
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}

    # Forward the request
    resp = requests.request(
        method=request.method,
        url=backend_url,
        headers=headers,
        params=request.args,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        stream=True
    )

    # Exclude hop-by-hop headers
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, response_headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
