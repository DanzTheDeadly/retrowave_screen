from yaml import safe_load
from http.server import BaseHTTPRequestHandler, HTTPServer

with open('conf.yaml') as conf_file:
    config = safe_load(conf_file)
print(config)


