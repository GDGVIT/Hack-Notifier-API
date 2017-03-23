from bs4 import BeautifulSoup
import requests

# List of things to scrape
# start_date, end_date, location, name, description, tags, url, type, deadline


def h_com():
    html_doc = requests.get('http://www.hackathon.com/country/india').text
    soup = BeautifulSoup(html_doc, 'html5lib')
    list_of_events = []
    for element in soup.find('div', attrs={'id': 'hackathonList'}).children:
        event = {}
        mny = element.find('div', attrs={'class':'hackathon-date-month-year'}).find(text=True, recursive=False)
        date = element.find('div', 'hackathon-date-day').text + ' ' + mny
        event['start_date'] = date.replace('\xa0', ' ')
        event['end_date'] = event['start_date']
        event['name'] = element.find('p', 'hackathon-name').text
        event['location'] = element.find('p', 'hackathon-location').text.replace(' -  ', ',')
        event['description'] = element.find('p', 'hackathon-desc hidden-xs').text.replace('\xa0', ' ')
        if element.find('p', 'hidden-xs hackathon-tags'):
            event['tags'] = [i.text for i in element.find('p', 'hidden-xs hackathon-tags').children]
        else:
            event['tags'] = []
        html_link = requests.get('http://www.hackathon.com' + element.find('p', 'hackathon-name').find('a')['href'])
        soup_link = BeautifulSoup(html_link.text, 'html5lib')
        event['url'] = soup_link.find('div', 'detail-buttons').find('a')['href']
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
        list_of_events.append({})

        list_of_events[-1]['start_date'], list_of_events[-1]['end_date'], list_of_events[-1]['location'] = element.find('tbody').find('div').text.split(' - ')
        list_of_events[-1]['start_date'] = f(list_of_events[-1]['start_date'].replace(',', '').split(' '))
        list_of_events[-1]['end_date'] = f(list_of_events[-1]['end_date'].replace(',', '').split(' '))

        list_of_events[-1]['name'] = element.find('a').text

        list_of_events[-1]['tags'] = None
        list_of_events[-1]['type'] = 'conference'
        list_of_events[-1]['description'] = None
        list_of_events[-1]['deadline'] = element.find('td', attrs={'style': 'padding:1px;margin:0px;text-align:right;vertical-align:middle;width:115px;'}).text[5:]

        list_of_events[-1]['url'] = element.find('tbody').contents[2].find('a').text
    return list_of_events


def vencity():
    html_doc = requests.get('http://www.venturesity.com/challenge/').text
    soup = BeautifulSoup(html_doc, 'html5lib')
    list_of_events = []
    for element in soup.find_all('div', 'col-lg-3 col-md-6 col-sm-6'):
        if '/challenge/id/' not in element.find('a')['href'] or element.find('div', 'col-md-12 col-sm-12 center').find('a').text != 'Register':
            continue
        list_of_events.append({ })
        list_of_events[-1]['name'] = element.find('div', 'course_info col-md-12 col-sm-12').find('h4').text
        list_of_events[-1]['deadline'] = None
        list_of_events[-1]['type'] = 'hackathon'
        list_of_events[-1]['tags'] = element.find('div', 'cat_row').text.replace('\n', '').replace('\t', '').split(',')
        list_of_events[-1]['url'] = 'http://www.venturesity.com' + element.find('div', 'photo').find('a')['href']
        html_link = requests.get(list_of_events[-1]['url']).text
        soup_link = BeautifulSoup(html_link, 'html5lib')
        list_of_events[-1]['start_date'] = soup_link.find('div', 'col-md-6 date-start')('span')[0].text.split(' - ')[0]
        list_of_events[-1]['end_date'] = soup_link.find('div', 'col-md-6 date-end')('span')[0].text.split(' - ')[0]
        list_of_events[-1]['description'] = soup_link.find('div', 'box_style_1')('p')[0].text
        list_of_events[-1]['location'] = soup_link.find('p', attrs={'id': 'challenge-location'}).text
    return list_of_events

