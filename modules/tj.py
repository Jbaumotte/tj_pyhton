##########################################################################
##Personal project - Joao Paulo Baumotte
##Name: Tribunal
##October 2013
##From a given file number, extract from the justice court web site
##the relevant information from the file and place it in a convinient and easy
##to look up database
#########################################################################

##import library to do http requests:
import urllib

##import beautiful soup parser:
from bs4 import BeautifulSoup

def get_page(num_processo):

    ##getting the url
    url = get_url(num_processo)
    
    ##download the file:    
    html = urllib.urlopen(url)

    ##convert to string:
    page = html.read()

    ##close file because we dont need it anymore:
    html.close()

    ##parse the file downloaded
    soup = BeautifulSoup(page, "xml")

    ## Isolating the relevant information
    reu = soup.find(id="i_nomeReu")["value"].encode('latin1')
    processo = soup.find(id="i_numeroProcesso14")["value"]
    classe = soup.find(id="i_classeProcessual")["value"].encode('latin1')
    crime = soup.find("table").find_all("td")[5].p
    crime = crime.get_text(strip=True).encode('latin1')
    relator = soup.find("table").find_all("td")[18].p
    relator = relator.get_text(strip=True).encode('latin1')

    ## Establishing the role of my sector
    relator = ver_relator(relator)

    ## placing mask on file number
    processo = mascara_processo(processo)
    
    ## Checking if the prosecution was placed as the defendent by the website 
    ## and correcting it
    if reu == 'MINIST\xc9RIO P\xdaBLICO DO DISTRITO FEDERAL E TERRIT\xd3RIOS':
        reu = soup.find(id="i_nomeAutor")["value"].encode('latin1')
    
    ## Making the defendent`s name shows in the correct manner (first letter 
    ## only in capital)
    reu = reu.title()
    
    return reu, classe, processo, crime, relator


def get_url(num_processo):
    
    ## depending on the way the file number is inputed by the user diferent web address must be used
    if len(str(num_processo)) < 9:
        url = "http://tjdf19.tjdft.jus.br/cgi-bin/tjcgi1?NXTPGM=plhtml06&ORIGEM=INTER&CDNUPROC="+str(num_processo)
			
    else:
        url = 'http://tjdf19.tjdft.jus.br/cgi-bin/tjcgi1?SELECAO=1&COMMAND=ok&CHAVE='+str(num_processo)+"&TitCabec=2%AA+Inst%E2ncia+%3E+Consulta+Processual&NXTPGM=plhtml02&ORIGEM=INTER"
        
    return url

def ver_relator(relator):
    if relator == 'Des\xaa. NILSONI DE FREITAS':
        relator = "Relatora"

    else:
        relator = "Revisora"

    return relator

def mascara_processo (num):
    new_num = num[:4]+"."+num[4:6]+"."+num[6:7]+"."+num[7:13]+"-"+num[13]
    return new_num
