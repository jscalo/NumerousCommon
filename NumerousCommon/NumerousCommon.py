import urllib
import urllib2
import re
import json
import sys
import base64
import requests

def _headers(apiKey):
    authStr = "Basic {0}".format(base64.b64encode(apiKey+":"))
    return {"Content-type": "application/json", "Authorization": authStr}

def _apiURLForPath(path, useV2=False):
    if useV2:
        base = "https://api.numerousapp.com/v2/"
    else:
        base = "https://api.numerousapp.com/v1/"
    return "{0}{1}".format(base, path)

def updateMetricValue(apiKey, metricID, value):
    url = _apiURLForPath("metrics/{0}/events".format(metricID))
    data = json.dumps({"value": float(value), "onlyIfChanged" : True})
    request = urllib2.Request(url, data, _headers(apiKey))
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print "http status: ", str(e.code)

def postMetricEvent(apiKey, metricID, event):
    url = _apiURLForPath("metrics/{0}/events".format(metricID))
    data = json.dumps(event)
    request = urllib2.Request(url, data, _headers(apiKey))
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print "http status: ", str(e.code)

def putMetric(apiKey, metric):
    url = _apiURLForPath("metrics/{0}".format(metric["id"]))
    data = json.dumps(metric)
    request = urllib2.Request(url, data, _headers(apiKey))
    request.get_method = lambda: 'PUT'
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print "http status: ", str(e.code)

def fetchMetric(apiKey, metricID):
    url = _apiURLForPath("metrics/{0}".format(metricID))
    request = urllib2.Request(url, None, _headers(apiKey))
    try:
        response = urllib2.urlopen(request)
        jsonData = json.load(response)
        return jsonData
    except urllib2.HTTPError, e:
        print "http status: ", str(e.code)

def uploadPhotoForMetric(apiKey, metricID, file, mimeType="image/jpeg"):
    url = _apiURLForPath("metrics/{0}/photo".format(metricID))
    mpart = { 'image' : ( 'image.img', file, mimeType) }
    authTuple = ( apiKey, '' )   
    request = requests.request('POST', url, auth=authTuple, data=None, files=mpart, headers=None)

def makeMetric(apiKey, metric):
    url = _apiURLForPath("metrics")
    data = json.dumps(metric)
    request = urllib2.Request(url, data, _headers(apiKey))
    try:
        response = urllib2.urlopen(request)
        jsonData = json.load(response)
        return jsonData  
    except urllib2.HTTPError, e:
        print "http status: ", str(e.code)

