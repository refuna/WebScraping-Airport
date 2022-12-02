from Orange.data import *
from lxml import etree
import requests
from bs4 import BeautifulSoup


Regions = ["Africa", "Americas", "Asia", "Europe", "Oceania"]
url = 'https://en.wikipedia.org/wiki/List_of_international_airports_by_country'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

df = []

for region in soup.select('h2'):
    found = region.findChild("span", text=Regions)
    if found:
        Region = found.text
        for subregion in region.next_siblings:
            if subregion.name == 'h2':
                break
            if subregion.name == 'h3':
                SubRegion = subregion.findChild("span", {"class":"mw-headline"}).text
                # print(Region+ " > " + SubRegion)
                bH4BeforeTable = False
                for country in subregion.next_siblings:
                    if country.name == 'h3':
                        break
                    if country.name == 'h4':
                        bH4BeforeTable = True
                        Country = country.findChild("span" , {"class":"mw-headline"}).text
                        for table in country.next_siblings:
                            if table.name == 'h4':
                                break
                            if table.name == 'table':
                                City =''
                                for tr in table.select("tr"):
                                    if tr.find('th'):
                                        continue
                                    tdlist = tr.select('td')
                                    if len(tdlist) >= 3:
                                        City = tdlist[0].text.strip()
                                        Airport = tdlist[1].text.strip()
                                        IAIACode = tdlist[2].text.strip()
                                        df.append([Region, SubRegion, Country, City, Airport, IAIACode])
                                    elif len(tdlist) <= 1:
                                        continue
                                    else:
                                        Airport = tdlist[0].text.strip()
                                        IAIACode = tdlist[1].text.strip()                                   
                                        df.append([Region, SubRegion, Country, City, Airport, IAIACode])
                    if (not bH4BeforeTable ) and country.name == 'table':
                        City =''
                        for tr in country.select("tr"): 
                            if tr.find('th'):
                                continue
                            tdlist = tr.select('td')
                            if len(tdlist) >= 3:
                                City = tdlist[0].text.strip()
                                Airport = tdlist[1].text.strip()
                                IAIACode = tdlist[2].text.strip()
                                df.append([Region, SubRegion, Country, City, Airport, IAIACode])
                            else:
                                Airport = tdlist[0].text.strip()
                                IAIACode = tdlist[1].text.strip()                                   
                                df.append([Region, SubRegion, Country, City, Airport, IAIACode])   

# import pandas as pd
# df_airport = pd.DataFrame(df, columns=['Region', 'SubRegion', 'Country', 'City', 'AirportName', 'IAIACode'] )
# print(df_airport)
                
                                    
region = StringVariable('region')
subRegion = StringVariable('subRegion')
country = StringVariable('country')
city = StringVariable('city')
airport = StringVariable('airport')
iata = StringVariable('iata')
domain = Domain([], metas=[region, subRegion, country, city, airport, iata])
table = Table.from_list(domain, df)
out_data = table
print(out_data)