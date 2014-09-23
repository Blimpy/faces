from bs4 import BeautifulSoup
from urllib2 import urlopen

def get_age_links(person_url): # goes to a person url and returns a pair: [photo_url, age]

    html = urlopen(person_url).read()
    soup = BeautifulSoup(html)
    text = soup.get_text()
    photoAge = []
    agesplit = text.split("Age:")  #splits text on word "Age:"
    if len(agesplit) == 2 :
        agestr = agesplit[1][1]+agesplit[1][2]
        age = int(agestr)

        img_link = soup.find(itemprop="image")
        if img_link != None:
            linky = img_link.get("href")
            photoAge = [age,linky]
    return photoAge




def get_name_links(base_url):  # gets a list of urls for specific people from base_url
    name_links = []
    all_links = []
    for i in range(1,84):  #cycle through pages: this gives 1000 people
        page_url = base_url + "?page=" + str(i)  #append page number
        html = urlopen(page_url).read()
        soup = BeautifulSoup(html, "lxml")
        for link in soup.find_all('a'):
            s_link = link.get('href')
            if '/US-Counties/District-of-Columbia/Unsorted-DC/' in s_link:
                s_link = 'http://mugshots.com'+s_link
                name_links.append(s_link)

    name_links.pop(0) #gets rid of the base_url which is always listed

    return name_links

def main():
    ctr = 0
    base_url = "http://mugshots.com/US-Counties/District-of-Columbia/Unsorted-DC/"
    name_links = get_name_links(base_url)
    al = [] # a list of pairs: [photo_url,  age]
    record = open("photos_by_ages.txt", "wb")
    for link in name_links:
        al_instance = get_age_links(link)
        if len(al_instance) == 2:
            al.append(al_instance)
            record.write(str(al_instance[0])+ ","+ al_instance[1] +"\n" )
            ctr+=1
            print(ctr)
    record.close()

    print("done, ctr is ", ctr)
    return 0

main()