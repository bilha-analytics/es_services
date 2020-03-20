import util_readerz
import nltk
import string


sourcez = {
    "Wikipedia 1": r"https://en.wikipedia.org/wiki/Timeline_of_the_2019%E2%80%9320_coronavirus_pandemic_in_February_2020",
    "Wikipedia 2" : r"https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic",
    #"MOH intro" : r"http://www.health.go.ke/covid-19/",  # lots of pdfs to parse 
    "NM article1": r"https://www.nation.co.ke/news/Covid-19-world-struggles-to-stop-handshake/1056-5497542-a0gos4z/index.html",
    "NM article2": r"https://www.nation.co.ke/newsplex/2718262-5496412-11gimflz/index.html",
    "NM article3" : r"https://www.nation.co.ke/oped/blogs/dot9/ndemo/2274486-5492926-awxihq/index.html",
    "Norwat article1" : r"https://www.norway.no/contentassets/ab00f23534c844bb961df1fadc9e44a8/information-note-regarding-ncovid-19-domestic-procedures-20200312_-final.pdf", 
    "Economist article1" : r"https://www.economist.com/europe/2020/02/23/italy-faces-a-sudden-surge-in-covid-19-cases",
    "MOH press release" : r"http://www.health.go.ke/wp-content/uploads/2020/03/press-statement-19th-march.pdf", 
    "CDC Situation Summary" : r"https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/summary.html",
    "CDC Home Self-care" : r"https://www.cdc.gov/coronavirus/2019-ncov/if-you-are-sick/caring-for-yourself-at-home.html",
    "CDC Facility Control" : r"https://www.cdc.gov/coronavirus/2019-ncov/infection-control/control-recommendations.html",
    "CDC Individual Control" : r"https://www.cdc.gov/coronavirus/2019-ncov/if-you-are-sick/steps-when-sick.html",
    "CDC Symptoms" : r"https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fabout%2Fsymptoms.html", 
    "CDC Clinical" : r"https://www.cdc.gov/coronavirus/2019-ncov/hcp/clinical-guidance-management-patients.html",
    "CDC LT Prep" : r"https://www.cdc.gov/coronavirus/2019-ncov/healthcare-facilities/prevent-spread-in-long-term-care-facilities.html",
    "CDC Discontinue Isolation" : r"https://www.cdc.gov/coronavirus/2019-ncov/hcp/disposition-in-home-patients.html",
    "WHO Intro" : r"https://www.who.int/health-topics/coronavirus",
    "WHO Director General" : r"https://www.who.int/dg/speeches/detail/who-director-general-s-opening-remarks-at-the-media-briefing-on-covid-19---11-march-2020",
    "WHO Individual Control" : r"https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public",
    "WHO Preparedness" : r"https://www.who.int/emergencies/diseases/novel-coronavirus-2019/technical-guidance/critical-preparedness-readiness-and-response-actions-for-covid-19",
    "WHO Africa cases" : r"https://www.afro.who.int/news/more-600-confirmed-cases-covid-19-africa", 

}

dashboardz = {
    "WHO Dashboard" : r"https://experience.arcgis.com/experience/685d0ace521648f8a5beeeee1b9125cd",

}

_sentz = []
_wordz = [] 
_vocab_lemmz = []

"""
    Fetch material online
    use newspaper3 to read online articles
    return list of documents 
"""
def readSiteContent():
    docz = []
    for item in sourcez.values():
        print( "Fetching {}".format(item) ) 
        docz.append( util_readerz.readNewsArtcile( item ) )

    print( len(docz) )
    
    return docz

"""
    Normalize tokens: lemmatize and remove stop words
""" 
def createCorpusSentenses():
    global _sentz, _wordz, _vocab_lemmz 
    docz = readSiteContent()
    for doc in docz: 
        _sentz += nltk.sent_tokenize( doc ) 
        print( "Count sentenses = {}".format(len(_sentz)) ) 
    
    _wordz = nltk.word_tokenize( " ".join(_sentz) ) 
    print( _sentz[:3])
    print( _wordz[: 5])  
    
'''
    Tokenize - Convert list of articles into list of sentences and list of words
    Normalize tokens: lemmatize and remove stop words
'''
def preProcessText(text):
    # prep tools   
    lemertizer = nltk.stem.WordNetLemmatizer() 
    punctuations = dict( (ord(p), None) for p in string.punctuation )

    # remove punctuations, change to lower case
    tokenz = nltk.word_tokenize( text.lower().translate( punctuations) ) 

    # build lemmz
    res = [ lemertizer.lemmatize( token )  for token in tokenz ] 

    return res 



if __name__ == "__main__":

    createCorpusSentenses()
    
    _vocab_lemmz = preProcessText( " ".join(_sentz ) ) 
    print( _vocab_lemmz[: 5])
    print("FIN: ==== {} sentences, {} words, {} lemma ====".format(len(_sentz), len(_wordz), len(_vocab_lemmz) ) )
