# noinspection PyUnresolvedReferences
import BaseHTTPServer
# noinspection PyUnresolvedReferences
import SimpleHTTPServer
import ssl

httpd = BaseHTTPServer.HTTPServer(('localhost', 8080), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./cert.pem', server_side=True)
httpd.serve_forever()
