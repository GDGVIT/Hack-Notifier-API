from bs4 import BeautifulSoup
from datetime import datetime
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# List of things to scrape
# start_date, end_date, location, name, description, tags, url, type, deadline


def h_com():
    return []
    html_doc = requests.get('https://www.hackathon.com/country/india', verify=False).text
    # return
    soup = BeautifulSoup(html_doc, 'html5lib')
    list_of_events = []
    # print(soup)
    for element in soup.find_all('div', attrs={'class': 'row'})[2]:
        # return
        event = {}
        try:
            st, en = element.find('div', attrs={'class': 'ht-eb-card__date'}).contents
        except ValueError:
            event['end_date'] = None
        else:
            event['end_date'] = ''
        std = st.find('div', attrs={'class': 'date__day'}).text + ' ' + st.find('div',
                                                                                attrs={'class': 'date__month'}).text
        event['start_date'] = std + " " + str(datetime.now().year)

        if event["end_date"] is not None:
            end = en.find('div', attrs={'class': 'date__day'}).text + ' ' + st.find('div',
                                                                                attrs={'class': 'date__month'}).text
            event['end_date'] = end + " " + str(datetime.now().year)
        # print(element)
        event['name'] = element.find('a', attrs={'class': 'ht-eb-card__title'}).text
        event['location'] = element.find('span', 'ht-eb-card__location__place').text
        event['description'] = element.find('div', attrs={'class','ht-eb-card__description'}).text.replace('\xa0','')
        event['url'] = None
        event['type'] = 'hackathon'
        event['deadline'] = None
        list_of_events.append(event)
    return list_of_events


def guide_conf():
    html_doc = requests.get('http://www.guide2research.com/conferences/IN').text
    soup = BeautifulSoup(html_doc, 'html5lib')
    list_of_events = []
    f = lambda x: str(x[1] + ' ' + x[0] + ' ' + x[-1])
    for element in soup.find_all('div', attrs={'style': 'margin-bottom:10px;padding:1px;', 'class': 'grey myshad'}):
        event = {}
        event['start_date'], event['end_date'], event['location'] = element.find('tbody').find('div').text.split(' - ')
        event['start_date'] = f(event['start_date'].replace(',', '').split(' '))
        event['end_date'] = f(event['end_date'].replace(',', '').split(' '))

        event['name'] = element.find('a').text

        event['type'] = 'conference'
        event['description'] = None
        event['deadline'] = element.find('td', attrs={
            'style': 'padding:1px;margin:0px;text-align:right;vertical-align:middle;width:115px;'}).text[5:]

        event['url'] = element.find('tbody').contents[2].find('a').text

        list_of_events.append(event)
    return list_of_events


def vencity():
    html_doc = requests.get('http://www.venturesity.com/challenge/').text
    soup = BeautifulSoup(html_doc, 'html5lib')
    list_of_events = []
    for element in soup.find_all('div', 'col-lg-3 col-md-6 col-sm-6'):
        if '/challenge/id/' not in element.find('a')['href'] or element.find('div', 'col-md-12 col-sm-12 center').find(
                'a').text != 'Register':
            continue
        event = {}
        event['name'] = element.find('div', 'course_info col-md-12 col-sm-12').find('h4').text
        event['deadline'] = None
        event['type'] = 'hackathon'
        event['url'] = 'http://www.venturesity.com' + element.find('div', 'photo').find('a')['href']
        html_link = requests.get(event['url']).text
        soup_link = BeautifulSoup(html_link, 'html5lib')
        event['start_date'] = soup_link.find('div', 'col-md-6 date-start')('span')[0].text.split(' - ')[0]
        event['end_date'] = soup_link.find('div', 'col-md-6 date-end')('span')[0].text.split(' - ')[0]
        event['description'] = soup_link.find('div', 'box_style_1')('p')[0].text
        event['location'] = soup_link.find('p', attrs={'id': 'challenge-location'}).text

        list_of_events.append(event)
    return list_of_events


if __name__ == "__main__":
    print(h_com())
    # print(guide_conf())
    # print(vencity())
