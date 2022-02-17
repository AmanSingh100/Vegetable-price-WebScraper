
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os



#from 7-20 to get state wise website
price_link = "https://market.todaypricerates.com/vegetables-daily-price"    #website from which we are getting state-wise vegetable prices
page_content = requests.get(price_link).text
soup = BeautifulSoup(page_content,'html.parser')

td1 = soup.find_all('td')   #finds the 'td' tags in table
for line_tag in td1:

    td1_tags = line_tag.find_all('a')   #finds all 'a' tags in the table
    for content_tags in td1_tags: 

        states_websites = "https://market.todaypricerates.com"+str(content_tags['href'])    #print websites state-wise | content_tags give 'href' content
        html_contents = requests.get(states_websites).text   #gets all html content of the website
        soup = BeautifulSoup(html_contents,'html.parser')
        state_name =  content_tags.get_text()    #get the state name | use when creating state-wise folders
        print(state_name)
       
        output_folder= ""      #give location of your output folder
        prices = os.path.join(output_folder,state_name)
        print(output_folder)
        if os.path.isdir(prices)==False:
            os.mkdir(prices)
        else:
            pass
                
        
        links = soup.find_all('table', attrs={'class':'shop_table'}) #website from which we are scraping href tag data
        for tag in links:
            tdtags = tag.find_all('a')
            for tags in tdtags: 
                addresses = "https://market.todaypricerates.com"+str(tags['href'])  #website from which we are scraping relevant info and updating it after  for next city
                html_contents = requests.get(addresses).text
                soup = BeautifulSoup(html_contents,'html.parser')
                tag1 = tags.get_text()
                # print(tag1) <--to check we are getting correct city
                # print(addresses) <--to check if were are getting correct website
                for address in addresses:

                    heading = []
                    all_data = {}
                    # get the table data
                    tbl_data = soup.find('div',attrs={'class':'Table'})
                    cell_list = []
                    table_data = []
                    # get the table headers
                    tbl_headers = tbl_data.find_all('div',attrs={'class':'Cellth'})
                    for headers in tbl_headers:
                        heading.append(headers.text)
                    for data in tbl_data.find_all('div',attrs={'class':'Row'}):
                        for cell in tbl_data.find_all('div',attrs={'class':'Cell'}):
                            # get cell value in list for every row
                            cell_list.append(cell.text)
                        for key in heading:
                            for values in cell_list:
                                all_data[key]=values
                                cell_list.remove(values)

                                break
                        table_data.append(all_data.copy())

                    df = pd.DataFrame(table_data)
                    df.to_csv(prices+'/'+str(tag1)+'_market.csv',index=False, encoding='UTF-8')