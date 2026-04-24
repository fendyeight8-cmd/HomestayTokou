import urllib.request
import tempfile
import sys

boundary = b'----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = (
    b'--' + boundary + b'\r\n'
    b'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n'
    b'Content-Type: image/jpeg\r\n\r\n'
    b'fake_image_content\r\n'
    b'--' + boundary + b'--\r\n'
)

req = urllib.request.Request('http://localhost:8080/api/upload', data=body, method='POST')
req.add_header('Content-Type', 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW')
req.add_header('Content-Length', str(len(body)))

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print('HTTP Error:', e.code, e.read().decode())
except Exception as e:
    print('Error:', e)
