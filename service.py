# -*- coding: utf-8 -*-
# used python-lambda (https://github.com/nficano/python-lambda) to set up environment
from urllib.request import urlopen
from nbconvert import HTMLExporter
import nbformat
import urllib

# Converts ipynb file referenced by the 'file' param (in the post request) and returns html.
# Ideally we would convert to pdf.  Tried using command line call (via subprocess), but it depends on TeX being installed (which is a heavy ask for the lambda environment).
# https://nbconvert.readthedocs.io/en/latest/install.html#installing-tex
def handler(event, context):
    try:
        site = urlopen(event['queryStringParameters']['file'])
        meta = site.info()
        contentLength = int(meta.get_all('Content-Length')[0])
        # print ("Content-Length:", contentLength)
        if contentLength > 26214400:
            raise ValueError('Notebook file is too large. It must be less than 25MB: ' + event.get('file'))
        response = site.read().decode()
        notebook = nbformat.reads(response, as_version=4)
        html_exporter = HTMLExporter()
        html_exporter.template_file = 'basic'
        (body, resources) = html_exporter.from_notebook_node(notebook)
        return {
            "statusCode": 200,
            "headers": { 
                "Content-Type": "text/html",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Expose-Headers": "Access-Control-Allow-Origin",
                "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
            },
            "body": body
        }
    except urllib.error.HTTPError as e:
        return {
            "statusCode": e.getcode(),
            "body": e.read()
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": e.args
        }
