'''
author: bg
goal: Read/Fetch from different text container/storage types. Write to different storage 
type: util, factory
refactor: class
'''
import zlogger

import pickle, json
from PyPDF2 import PdfFileReader as pdf 
from newspaper import Article



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
        raise NotImplementedError
    elif mode == MODE_APPEND:
        raise NotImplementedError 
    else:
        pass
    
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
        pass

    return results 

## Case: Multiple web pages
def doWebSite(dpath, mode=MODE_READ, content=None):
    results = None

    if mode == MODE_WRITE:
        raise NotImplementedError
    elif mode == MODE_APPEND:
        raise NotImplementedError 
    else:
        pass
    
    return results 

## Case: serialize
def doPickle(dpath, mode, content=None):
    results = None

    if mode == MODE_WRITE:
        raise NotImplementedError
    elif mode == MODE_APPEND:
        raise NotImplementedError 
    else:
        pass
    
    return results 

## Case: Local file TODO: binary or not? 
def doFile(dpath, mode, content=None):
    results = None 

    if mode == MODE_WRITE:
        raise NotImplementedError 
    elif mode == MODE_APPEND:
        raise NotImplementedError
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
    res(dpath, mode) 





if __name__ == "__main__":
    zlogger.log( "dataSource.main", "Starting") 
    for ln in readFrom("example.txt") :
        print("\n\t{}\n".format(ln) ) 
    zlogger.log( "dataSource.main", "Finished") 

