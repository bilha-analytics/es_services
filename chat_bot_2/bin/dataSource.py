'''
author: bg
goal: Read/Fetch from different text container/storage types. Write to different storage 
type: util, factory
refactor: class
'''
import zlogger

import sys, traceback, os 

import pickle, json
from PyPDF2 import PdfFileReader as pdf 
from newspaper import Article
import newspaper
import urllib.request as url_req

# #GSheet read using Twilio opt
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

#GSheet read using TWDS Opt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow 
from google.auth.transport.requests import Request 

'''
Types of data source handlers 
TODO: number assignment, SQL, 
''' 
zJSON = 1
zARTICLE = 2
zNESTED_ARTICLES = 3
zPDF = 4
zSERIALIZED = 5
zGSHEET = 6
zFILE = 10

MODE_READ = 1
MODE_WRITE = 2
MODE_APPEND = 3



### --- HELPERS --- ###
'''
Input:
    path: url to resource
    mode: are we reading, overwriting or appending. Read mode as default for rarely written to resources 
    content: what are we writing. Default ss none b/c read mode. TODO: separation of roles 
Return:
    None if writing else content that's been read if reading  TODO: separation of roles 

TODO: **kwargs e.g. encoding @ txt, 
''' 
### --- end docstr --- ###

# Case: Json files and Streams??
def doJson(dpath, mode, content=None):
    results = None

    if mode == MODE_WRITE:
        with open(dpath, 'w') as df:
            json.dump( content, df ) 
    elif mode == MODE_APPEND:
        raise NotImplementedError 
    else:
        # with open( dpath) as df:
        with url_req.urlopen( dpath ) as df: 
            results = json.load( df ) 
    
    return results 

## Case: PDF Files 
def doPdf(dpath, mode=MODE_READ, content=None): 
    results = None 

    if mode == MODE_WRITE:
        raise NotImplementedError
    elif mode == MODE_APPEND:
        raise NotImplementedError 
    else:
        with open( dpath, "rb") as dfile:
            res = []
            doc = pdf( dfile )
            len = doc.getNumPages() # doc.numPages
            for i in range(len):
                res.append( doc.getPage(i).extractText() )
            results = " ".join( res )

    return results

## Case: Web page 
def doWebArticle(dpath, mode=MODE_READ, content=None):
    results = None

    if mode == MODE_WRITE:
        raise NotImplementedError
    elif mode == MODE_APPEND:
        raise NotImplementedError 
    else:
        article = Article( dpath )
        article.download() # fetch html
        article.parse( ) # parse for content and meta ; ready it for tokeninzer and nltk nlp 
        results = article.text 

    return results 

## Case: Multiple web pages
def doWebSite(dpath, mode=MODE_READ, content=None):
    results = None

    if mode == MODE_WRITE:
        raise NotImplementedError
    elif mode == MODE_APPEND:
        raise NotImplementedError 
    else:
        results = []
        site = newspaper.build( dpath )
        for article in site.articles:
            article.download()
            article.parse()
            results.append( article.text )
    
    return results 

## Case: serialize
def doPickle(dpath, mode, content=None):
    results = None

    if mode == MODE_WRITE:
        with open( dpath, "wb") as dfile:
            pickle.dump(content, dfile)
    elif mode == MODE_APPEND:
        with open( dpath, "ab") as dfile:
            pickle.dump(content, dfile)
    else:
        with open( dpath, "rb") as dfile:
            results = pickle.load( dfile )
    return results 

## Case: Local file TODO: binary or not? 
def doFile(dpath, mode, content=None):
    results = None 

    if mode == MODE_WRITE:
        with open( dpath, "w") as dfile:
            dfile.write( content ) 
    elif mode == MODE_APPEND:
        with open( dpath, "a") as dfile:
            dfile.write( content ) 
    else:
        with open( dpath, "r") as dfile:
            results = dfile.readlines() 

    return results


## Case GSheet read write 
def doGSheet(dpath, mode, content=None):
    results = None

    if mode == MODE_WRITE:
        raise NotImplementedError
    elif mode == MODE_APPEND:
        raise NotImplementedError 
    else: 
        results = gsheetRead_GoogleWay( dpath )
    return results 

# def gsheetRead_twilioOpt(dpath):    
#     scope = ['https://www.googleapis.com/auth/spreadsheets']
#     creds = ServiceAccountCredentials.from_json_keyfile_name('gsheet_get.json', scope)
#     clt = gspread.authorize( creds ) 
#     gsheet = clt.open( dpath ).sheet1
#     return gsheet.get_all_records()

## the Google Py API Way of reading sheets
def gsheetRead_GoogleWay(dpath):
    results = None
    
    scope =  ['https://www.googleapis.com/auth/spreadsheets'] 

    creds = None
    if os.path.exists( 'token.pickle'):
        with open( 'token.pickle', 'rb') as fd:
            creds = pickle.load( fd ) 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh( Request() ) 
        else:
            flow = InstalledAppFlow.from_client_secrets_file( 'gsheet_get.json', scope) 
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as fd:
            pickle.dump( creds, fd) 
    
    service = build('sheets', 'v4', credentials=creds, cache_discovery=False) 

    sheet = service.spreadsheets()
    reader = sheet.values().get(spreadsheetId=dpath[0], range=dpath[1]).execute() 
    
    # print( '>>>>> is JSON>=?',  reader )

    results = reader.get('values', None)  

    return results 
             
### ----------------------------------------------- 


STREAMZ = {
    zJSON : doJson,
    zARTICLE : doWebArticle,
    zNESTED_ARTICLES : doWebSite,
    zPDF : doPdf,
    zSERIALIZED : doPickle ,
    zGSHEET : doGSheet, 
}# default is doFile 

#TODO: define url to resource 

'''
Go to a given path and fetch the content. Up to the caller to parse the content as desired
Errors: Up to the caller to handle exceptions
Input:
    path: url to resource 
    dtype: type of resource. Default is a local text file 
Return: content fetched in whatever form it was stored. 
''' 
def readFrom( dpath, dtype=zFILE):
    res = STREAMZ.get(dtype, doFile) 
    return res(dpath, MODE_READ)  

'''
Given some data, write it to a give resource. Up to the caller to format data approporiately 
Errors: Up to the caller to handle exceptions
Input:
    content: what is to be written to file
    path: url to resource
    dtype: type of resource. Default is a local text file 
    mode: are we overwriting or appending. Default is to overwrite 
Return: 
''' 
def writeTo(content, dpath, dtype=zFILE, mode=MODE_WRITE):
    res = STREAMZ.get( dtype, doFile) 
    zlogger.log("dataSource.writeTo", "res = {}".format(res) )
    res(dpath, mode=mode,  content=content,)  





if __name__ == "__main__":
    zlogger.log( "dataSource.main", "Starting") 

    
    arange = 'FAQ responses!A1:G1000'
    gsheet_id = '1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks' #covid_19_faq
    # gsheet_id = 'covid_19_faq'

    etype = ['Text File', 'PDF', 'Article', 'Site', 'Serialized', 'GSheet']
    etype_i = [zFILE, zPDF, zARTICLE, zNESTED_ARTICLES, zSERIALIZED, zGSHEET]
    epath = ['example.txt', 'example.pdf', 'https://www.nation.co.ke/counties/nairobi/Police-kill-ATM-heist-mastermind/1954174-5503356-aodphx/index.html', 'https://www.standardmedia.co.ke/corporate/news', 'example.byt', (gsheet_id, arange) ]
    econtent = ['The quick brown fox jumper over the lazy dogs.'*7, None, None, None, dict((k, v) for k, v in zip(etype, epath)), None]


    for et, ei, ep, ec in zip( etype, etype_i, epath, econtent):
        print( "\n{0} {1} {0}\n{2}\n".format( "-"*7, et, ep ) ) 
        try:
            # for ln in readFrom(ep, dtype=ei) :     
            ln = readFrom(ep, dtype=ei)
            print("\n\t{}\n".format(ln) ) 
        except:
            zlogger.logError("dataSource.main.readExample", "EXCEPT: {} - {}".format(et, ep) ) 

        try:
            writeTo(ec, ep, dtype=ei) 
        except:
            zlogger.logError("dataSource.main.writeExample", "EXCEPT: {} - {}".format(et, ep) ) 
    
    zlogger.log( "dataSource.main", "Finished") 

