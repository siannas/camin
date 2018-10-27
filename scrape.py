import urllib.request
from bs4 import BeautifulSoup

def cariKerja ():
    url = 'https://www.jobstreet.co.id/id/job-search/job-vacancy.php?ojs=1'
    #---------------Make_connection_https--------------#
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    con = urllib.request.urlopen(req)
    page = BeautifulSoup(con, 'html.parser')
    
    #containers = page.body.div.find("div", "container").div
    containers = page.find(id="job_listing_panel")
    #print(containers)
    
    result = {}
    idx = 1
    while idx <= 3:
        id_tag = "job_ad_"+ str(idx)
        cntr = containers.find("div",id=id_tag) 
        
        gambar = cntr.find("img", "img-company-logo")['data-original']
        job = cntr.find("h2").text
        company = cntr.h3.a.span.text
        lokasi = cntr.ul.li.span.text
        link = cntr.find("div", "position-title").a['href']
        
        result[idx] = {
            "gambar":gambar,
            "job":job,
            "company" :company,
            "lokasi":lokasi,
            "link":link
        }
        
        idx += 1
    #print(result)
    return result
