from turtle import ht
import requests
import mysql.connector
from bs4 import BeautifulSoup
# use to parse html text
from lxml.html import fromstring 
from itertools import cycle
import traceback
from fake_useragent import UserAgent
#reference code
# def web(page,WebUrl):
#      if(page>0):
#         url = WebUrl
#         code = requests.get(url)
#         plain = code.text
#         s = BeautifulSoup(plain, "html.parser")
#         for link in s.findAll('a', {'class':'nav_a'}): #s-access-detail-page  nav_a icp-button
#             tet = link.get('title')
#             print(tet)
#             tet_2 = link.get('href')
#             print(tet_2)
#web(1,'https://www.amazon.in/mobile-phones/b?ie=UTF8&node=1389401031&ref_=nav_shopall_sbc_mobcomp_all_mobiles')

def to_get_proxies():
    # website to get free proxies
    url = 'https://free-proxy-list.net/'
 
    response = requests.get(url)
 
    parser = fromstring(response.text)
    # using a set to avoid duplicate IP entries.
    proxies = set() 
    
    for i in parser.xpath('//tbody/tr')[:250]:
        # to check if the corresponding IP is of type HTTPS
        if i.xpath('.//td[7][contains(text(),"yes")]')!=-1:
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                              i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies






def world_chalice_crawler(WebUrl):
    #CREATE DB THERE IF NEED TO
    #mycursor.execute("CREATE DATABASE pszproject") - do this after establishing a connection without db name
    #and then connect again, with the same method "connect", but with the additional field regarding the database

    #connect to the db
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database = "pszproject"
        #password="mypassword"
    )
    mycursor = mydb.cursor()
    #create a table
    rows = ""
    rows +="id INT PRIMARY KEY AUTO_INCREMENT, stanje VARCHAR(255), marka VARCHAR(255), model VARCHAR(255), godiste INT, kilometraza INT, "
    rows += "kubikaza INT, snaga INT, motor VARCHAR(255), pogon VARCHAR(255), menjac VARCHAR(255), brzine VARCHAR(255), vrata VARCHAR(255), sedista INT, "
    rows += "volan VARCHAR(255), klima VARCHAR(255), boja VARCHAR(255), boja_unutra VARCHAR(255), karoserija VARCHAR(255), lokacija VARCHAR(255), "
    rows += "gorivo VARCHAR(255), cena INT"
    query = "CREATE TABLE if not exists big_kola ("+ rows+ ")"
    mycursor.execute(query)
    #prepare proxies
    proxies = to_get_proxies()
    proxyPool = cycle(proxies)     
    # #set up user agent
    # ua = UserAgent()
    #start crawling
    url = WebUrl
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    #jedna strana paginacije
    #845 je bezbedan broj stranica
    for i in range(123): #za sad u opsegu 20, promenicemo posle
        print("i: ", i)
        #j = 0
        #pojedinacni automobil
        titles = s.find_all('div', {"class":"addTitleWrap"})
        for title in titles:
            link = title.find('a', {"class":"addTitle"})
            #print("j:", j)
            #za svaki automobil postoje po 2 linka koja vode do informacija o njemu, pa neparni
            # if (j%2==1):
            #     j+=1
            #     continue
            #dohvatamo link tog automobila
            #https://www.mojauto.rs/polovni-automobili/3143445_Smart_ForTwo_2017_god/?cena=high
            #/polovni-automobili/3143445_Smart_ForTwo_2017_god/?cena=high'
            exact_car_url = "https://www.mojauto.rs/" + link.get('href')
            exact_car_code = requests.get(exact_car_url)
            exact_car_plain = exact_car_code.text

            exact_car_s = BeautifulSoup(exact_car_plain, "html.parser")        
            #obrada automobila
            car_name = exact_car_s.find('div', {"class":"singleTop"}).find("h1").get_text()
            #print(car_name)
            #datashape: {"key":value}
            #single info approach: tech_specs[index]["key"]
            tech_specs = []
            tech_spec_list = exact_car_s.find('ul', {"class": "techSpec"})
            #{key:val} je dictionary, (ket, val) je tuple
            for list_elem in tech_spec_list.find_all("li"):
                tech_specs.append({list_elem.find("span").get_text():list_elem.find("strong").get_text()}) 
            brand_and_model = car_name.split(" ")
            brand = brand_and_model[0]
            model = brand_and_model[1]
            cena = exact_car_s.find("span", {"class":"priceReal"}).text.split(" ")[0]
            if cena.find(".") !=-1:
                hiljade = cena.split(".")[0]
                stotine = cena.split(".")[1]
                cena = int(hiljade + stotine)
                #print(cena)
            else:
                cena = None
            #sad preskoci stanje, marku, model, godiste, gorivo, lokaciju
            kilometraza = 0
            kubikaza = 0
            snaga = 0
            motor = ""
            pogon = ""
            menjac = ""
            brzine = ""
            vrata = ""
            sedista = 0
            volan = ""
            klima = ""
            boja = ""
            boja_unutra = ""
            karoserija = ""
            godiste = 0
            gorivo = "" #inicijalno je prazno, ako nema informacije o tome na sajtu
            for k in range(len(tech_specs)):
                if "Kubikaža" in tech_specs[k]:
                    try:
                        kubikaza = int(tech_specs[k]["Kubikaža"].split(" ")[0])
                    #Svaki recnik ima jednu rec samo, pa kad nadje, da ne ispituje dalje
                        continue
                    except:
                        kubikaza = 150
                    #Svaki recnik ima jednu rec samo, pa kad nadje, da ne ispituje dalje
                        continue

                if "Prešao kilometara" in tech_specs[k]:
                    kilometraza = int(tech_specs[k]["Prešao kilometara"])
                    continue
                if "Snaga" in tech_specs[k]:
                    snaga = int(tech_specs[k]["Snaga"].split()[0])
                    continue
                if "Tip motora" in tech_specs[k]:
                    motor = tech_specs[k]["Tip motora"]
                    continue
                if "Pogon" in tech_specs[k]:
                    pogon = tech_specs[k]["Pogon"]
                    continue
                if "Menjač" in tech_specs[k]:
                    menjac = tech_specs[k]["Menjač"]
                    continue
                if "Broj brzina" in tech_specs[k]:
                    brzine = tech_specs[k]["Broj brzina"]
                    continue
                if "Broj vrata" in tech_specs[k]:
                    vrata = tech_specs[k]["Broj vrata"]
                    continue
                if "Broj sedišta" in tech_specs[k]:
                    sedista = int(tech_specs[k]["Broj sedišta"])
                    continue
                if "Strana volana" in tech_specs[k]:
                    volan = tech_specs[k]["Strana volana"]
                    continue
                if "Klima" in tech_specs[k]:
                    klima = tech_specs[k]["Klima"]
                    continue
                if "Boja" in tech_specs[k]:
                    boja = tech_specs[k]["Boja"]
                    continue
                if "Boja unutrašnjosti" in tech_specs[k]:
                    boja_unutra = tech_specs[k]["Boja unutrašnjosti"]
                    continue
                if "Kategorija" in tech_specs[k]:
                    karoserija = tech_specs[k]["Kategorija"]
                    continue

            # print('brand: ', brand)
            # print("model: ", model)
            basicData = exact_car_s.find('ul', {"class":"basicSingleData"})
            #sredi GODISTE, GORIVO
            fuel_and_year_list = basicData.find_all("li")
            for fy_list_elem in fuel_and_year_list:
                span_list = fy_list_elem.find_all("span")
                for span_elem in span_list:
                    if span_elem.get_text().find("godište") != -1:
                        godiste = int(span_elem.get_text().split(".")[0])
                        #print(godiste)
                    if span_elem.get_text().find("Benzin") != -1:
                        gorivo = "Benzin"
                        #print(gorivo)
                    if span_elem.get_text().find("Električno") != -1:
                        gorivo = "Električno"
                        #print(gorivo)
                    if span_elem.get_text().find("Hibrid") != -1:
                        gorivo = "Hibrid"
                        #print(gorivo)
                    if span_elem.get_text().find("Metan CNG") != -1:
                        gorivo = "Metan"
                        #print(gorivo)
                    if span_elem.get_text().find("Gas (TNG) benzin") != -1:
                        gorivo = "Gas (TNG) benzin"
                        #print(gorivo)
                    if span_elem.get_text().find("Ostalo") != -1:
                        gorivo = "Ostalo"
                        #print(gorivo)   
            #godiste = basicData.find_all("li")[1].find_all("span")[0].get_text().split(".")[0] #split razdvaja 2017.godiste na 2017 i godiste, zelim brojcanu vrednost
            #gorivo = basicData.find_all("li")[3].find_all("span")[1].get_text()
            sellerInfo = exact_car_s.find("div", {"class":"sellerInfoText"})
            lokacija = sellerInfo
            if(lokacija==None):
                lokacija = ""
            else:
                lokacija = lokacija.text.split("\n")[2]
                lokacija = lokacija.strip()
                lokacija_word_by_word = lokacija.split(" ")
                lokacija = ""
                for iter in range(len(lokacija_word_by_word)):                    
                    lokacija += lokacija_word_by_word[iter].capitalize()
                    if(iter!=len(lokacija_word_by_word)-1):
                        lokacija+=" "
            try:
                html_sa_stanjem = exact_car_s.find_all("div", {"class":"singleBox"})[2]
            # html_sa_stanjem = html_sa_stanjem.text
            # html_sa_stanjem = BeautifulSoup(html_sa_stanjem, "html.parser")
            
                stanje = html_sa_stanjem.find_all("li")[1].find("strong").text.capitalize()
            except:
                stanje = "Polovno"
            sql = "INSERT INTO big_kola (stanje, marka, model, godiste, kilometraza, kubikaza, snaga, motor, pogon, menjac, brzine, vrata, sedista,"
            sql+= "volan, klima, boja, boja_unutra, karoserija, lokacija, gorivo, cena)"
            # %s se koristi kao ? u JDBC, nema veze sa oznacavanjem stringa/broja, dakle ne treba mi %d nigde
            #sql+="VALUES (%s, %s, %s, %d, %d, %d, %d, %s, %s, %s, %d, %s, %d, %s, %s, %s, %s, %s, %s, %s)"
            sql+="VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (stanje, brand, model, godiste, kilometraza, kubikaza, snaga, motor, pogon, menjac, brzine, vrata, sedista, volan,
            klima, boja, boja_unutra, karoserija, lokacija, gorivo, cena)
            #print(val)
            mycursor.execute(sql, val)
            mydb.commit()
            
            #j+=1										
        #azuriram url
        
        next_page = s.find('a', {'class':'pag_next'})
        #print(next_page)
        #https://www.mojauto.rs/rezultat/status/automobili/vozilo_je/polovan/poredjaj-po/oglas_najnoviji/po_stranici/20/prikazi_kao/lista/stranica/3
        url="https://www.mojauto.rs" +next_page.get("href")
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        #OVDE RADIM AZURIRANJE PROXIJA
        # while True:
        #     proxy = next(proxyPool)
        #     #print(proxy)
        #     try:
        #         code = requests.get(url, proxies={"http": proxy, "https": proxy})
        #         plain = code.text
        #         s = BeautifulSoup(plain, "html.parser")
        #         break
        #     except:
        #         #print("zabo")
        #         continue
        # print('prosao glupu petlju')
        # print(proxy)
        # while True:
        #     try:
        #         header = {'User-Agent':str(ua.random)}
        #         code = requests.get(url, headers=header)
        #         plain = code.text
        #         s = BeautifulSoup(plain, "html.parser")
        #         break
        #     except:
        #         print("zabo")
        #         continue
        # print('prosao glupu petlju')



#https://www.mojauto.rs/rezultat/status/automobili/vozilo_je/polovan/poredjaj-po/oglas_najnoviji/po_stranici/20/prikazi_kao/lista/
world_chalice_crawler("https://www.mojauto.rs/rezultat/status/automobili/poredjaj-po/oglas_najnoviji/po_stranici/20/prikazi_kao/lista/stranica/723") #i ovaj rade https://www.mojtrg.rs  https://www.mojauto.rs

def empty_db(mycursor):
    mycursor.execute("DELETE * FROM big_kola")


