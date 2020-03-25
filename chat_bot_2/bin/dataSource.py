'''
author: bg
goal: Read/Fetch from different text container/storage types. Write to different storage 
type: util, factory
refactor: class
'''
import zlogger, logging

import sys, traceback

import pickle, json
from PyPDF2 import PdfFileReader as pdf 
from newspaper import Article
import newspaper
import urllib.request as url_req

'''
Types of data source handlers 
TODO: number assignment, SQL, 
''' 
zJSON = 1
zARTICLE = 2
zNESTED_ARTICLES = 3
zPDF = 4
zSERIALIZED = 5
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


### ----------------------------------------------- 


STREAMZ = {
    zJSON : doJson,
    zARTICLE : doWebArticle,
    zNESTED_ARTICLES : doWebSite,
    zPDF : doPdf,
    zSERIALIZED : doPickle ,
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


    etype = ['Text File', 'PDF', 'Article', 'Site', 'Serialized']
    etype_i = [zFILE, zPDF, zARTICLE, zNESTED_ARTICLES, zSERIALIZED]
    epath = ['example.txt', 'example.pdf', 'https://www.nation.co.ke/counties/nairobi/Police-kill-ATM-heist-mastermind/1954174-5503356-aodphx/index.html', 'https://www.standardmedia.co.ke/corporate/news', 'example.byt']
    econtent = ['The quick brown fox jumper over the lazy dogs.'*7, None, None, None, dict((k, v) for k, v in zip(etype, epath))]


    for et, ei, ep, ec in zip( etype, etype_i, epath, econtent):
        print( "\n{} {} {}\n{}\n".format( "-"*7, et, "-"*7, ep ) ) 
        try:
            # for ln in readFrom(ep, dtype=ei) :     
            ln = readFrom(ep, dtype=ei)
            print("\n\t{}\n".format(ln) ) 
        except:
            e = sys.exc_info()[0] 
            zlogger.log("dataSource.main.readExample", "EXCEPT: {} - {}:: {}".format(et, ep, e), ltype=logging.ERROR ) 
            print( traceback.format_exc() )

        try:
            writeTo(ec, ep, dtype=ei) 
        except:
            e = sys.exc_info()[0] 
            zlogger.log("dataSource.main.writeExample", "EXCEPT: {} - {}:: {}".format(et, ep, e), ltype=logging.ERROR ) 
            print( traceback.format_exc() )
    
    zlogger.log( "dataSource.main", "Finished") 

