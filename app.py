from bs4 import BeautifulSoup
import requests
import re
import sys

###########################################################
## HELPER FUNCTIONS
###########################################################

def getActorId(name: str) -> str:
    formattedName = name.replace(' ', '+')
    url = f'https://www.imdb.com/find/?q={formattedName}&s=nm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to access url", file=sys.stderr)
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find('a', href=re.compile(r'/name/(nm\d+)/'))

    if not result:
        print("Could not find the actor", file=sys.stderr)
        return None
    
    actorIdMatch = re.search(r'/name/(nm\d+)/', result['href'])

    if not actorIdMatch:
        print("Could not extract IMDB data for" + name, file=sys.stderr)
        return None
    
    actorId = actorIdMatch.group(1)

    return actorId

def scrapeActorAboutInfo(actorId: str) -> str:
    url = f'https://www.imdb.com/name/{actorId}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("About info - Cannot access url:" + url)
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    infoDiv = soup.find('div', class_='ipc-html-content-inner-div')

    return infoDiv.get_text()

def scrapeActorKnownFor(actorId: str) -> list[str]:
    url = f'https://www.imdb.com/name/{actorId}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Known for - Cannot access url:" + url)
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    knownForDivs = soup.find('div', class_='sc-a5610b27-0 jYtfvr').find_all('div', class_='ipc-primary-image-list-card__content-top')

    knownForTitles = []

    for knownForDiv in knownForDivs:
        title = knownForDiv.find('a', class_='ipc-primary-image-list-card__title').get_text()
        knownForTitles.append(title)

    return knownForTitles

def printActorKnownForTitles(titles: list[str]):
    print("Known for: ")

    for title in titles:
        print(f"{title}")

def scrapeUpcomingProjects(actorId: str) -> list[str]:
    url = f'https://www.imdb.com/name/{actorId}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Known for - Cannot access url:" + url)
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    upcomingProjectsDiv = soup.find('div', id='accordion-item-actor-upcoming-projects')
    if not upcomingProjectsDiv:
        upcomingProjectsDiv = soup.find('div', id='accordion-item-actress-upcoming-projects')

    if not upcomingProjectsDiv:
        return []
    
    upcomingProjectsContent = upcomingProjectsDiv.find('div', class_='ipc-accordion__item__content_inner accordion-content')
    if upcomingProjectsContent:
        upcomingProjects = upcomingProjectsContent.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between date-unrel-credits-list ipc-metadata-list--base')
        upcomingProjectsList = upcomingProjects.find_all('li', class_='ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-ee772624-0 eCnPST unreleased-credit')

        ActorUpcomingProjectsList = []

        for u in upcomingProjectsList:
            div = u.find('div', class_='ipc-metadata-list-summary-item__c').find('div', class_='ipc-metadata-list-summary-item__tc')
            titleElement = div.find('a', class_='ipc-metadata-list-summary-item__t')
            title = titleElement.get_text()

            roleList = div.find('ul')
            role = roleList.find('li').find('span')
            roleText = ''
            if role:
                roleText = role.get_text()

            if roleText:
                ActorUpcomingProjectsList.append(f'Title: {title}\t Role: {roleText}')
            else:
                ActorUpcomingProjectsList.append(f'Title: {title}')
        
        return ActorUpcomingProjectsList
    
    return None

def scrapeActorCredits(actorId: str) -> list[str]:
    url = f'https://www.imdb.com/name/{actorId}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Known for - Cannot access url:" + url)
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    creditsDiv = soup.find('div', id='accordion-item-actor-previous-projects')
    if not creditsDiv:
        creditsDiv = soup.find('div', id='accordion-item-actress-previous-projects')

    if not creditsDiv:
        return []
    
    creditsContent = creditsDiv.find('div', class_='ipc-accordion__item__content_inner accordion-content')
    if creditsContent:
        credits = creditsContent.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between ipc-metadata-list--base')
        creditsList = credits.find_all('li', class_='ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-d5824c4f-2 dhiRpX')

        actorCreditsList = []

        for c in creditsList:
            div = c.find('div', class_='ipc-metadata-list-summary-item__c').find('div', class_='ipc-metadata-list-summary-item__tc')
            titleElement = div.find('a', class_='ipc-metadata-list-summary-item__t')
            title = titleElement.get_text()

            roleList = div.find('ul')
            role = roleList.find('li').find('span')
            roleText = ''
            if role:
                roleText = role.get_text()

            if roleText != '':
                actorCreditsList.append(f'Title: {title}\t Role: {roleText}')
            else:
                actorCreditsList.append(f'Title: {title}')
        
        return actorCreditsList
    
    return None

def getShowId(name: str) -> str:
    formattedName = name.replace(' ', '+')
    url = f'https://www.imdb.com/find/?q={formattedName}&s=tt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to access url", file=sys.stderr)
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find('a', href=re.compile(r'/title/(tt\d+)/'))

    if not result:
        print("Could not find the actor", file=sys.stderr)
        return None
    
    showIdMatch = re.search(r'/title/(tt\d+)/', result['href'])

    if not showIdMatch:
        print("Could not extract IMDB data for" + name, file=sys.stderr)
        return None
    
    showId = showIdMatch.group(1)

    return showId

def scrapeShowRating(showId: str) -> str:
    url = f'https://www.imdb.com/title/{showId}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Rating - Cannot access url:" + url)
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    ratingSpan = soup.find('span', class_='sc-d541859f-1 imUuxf')
    if not ratingSpan:
        return "Invalid"
    
    rating = ratingSpan.get_text()

    return rating

def scrapeShowCreators(showId: str) -> list[str]:
    url = f'https://www.imdb.com/title/{showId}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Rating - Cannot access url:" + url)
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    creatorsDiv = soup.find('div', class_='ipc-metadata-list-item__content-container')
    creatorsList = creatorsDiv.find('ul')
    creators = creatorsList.find_all('li')

    list = []

    for c in creators:
        creatorElement = c.find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
        list.append(creatorElement.get_text())

    return list


def scrapeShowCast(showId: str) -> list[str]:
    url = f'https://www.imdb.com/title/{showId}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Rating - Cannot access url:" + url)
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    castDiv = soup.find('div', class_='ipc-shoveler ipc-shoveler--base ipc-shoveler--page0 title-cast__grid')
    castInnerDivs = castDiv.find_all('div', class_='sc-cd7dc4b7-5 intBIf')

    cast = []

    for castInnerDiv in castInnerDivs:
        castElement = castInnerDiv.find('a', class_='sc-cd7dc4b7-1 kVdWAO')
        castName = castElement.get_text()

        cast.append(castName)

    return cast

def scrapeShowAbout(showId: str) -> str:
    url = f'https://www.imdb.com/title/{showId}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Rating - Cannot access url:" + url)
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    showAbout = soup.find('span', class_='sc-42125d72-0 gKbnVu')
    showAboutText = showAbout.get_text()

    if showAboutText:
        return showAboutText
    else:
        return None


def printAList(l: list) -> None:
    for item in l:
        print(item)

###########################################################
## MAIN FUNCTION
###########################################################

if __name__ == "__main__":
    while True:
        print()
        print("Welcome to IMDB Scraper")
        print("=" * 50)
        print("1. Scrape by actor")
        print("2. Scrape movies and shows")
        print("0. Exit")
        print("=" * 50)
        choice = input("Enter choice: ")

        if choice == "1":
            actorName = input("Enter a name: ")

            print()

            actorId = getActorId(actorName)
            print("Actor ID:" + actorId)

            print()

            actorAboutInfo = scrapeActorAboutInfo(actorId)
            print(actorAboutInfo)

            print()

            actorKnownForTitles = scrapeActorKnownFor(actorId)
            printActorKnownForTitles(actorKnownForTitles)

            print()

            print("Upcoming Projects: ")
            actorUpcomingProjects = scrapeUpcomingProjects(actorId)
            if actorUpcomingProjects:
                printAList(actorUpcomingProjects)
            else:
                print("None")

            print()
            print("Previous credits:")
            actorCredits = scrapeActorCredits(actorId)
            if actorCredits:
                printAList(actorCredits)
            else:
                print("None")
            
            print()
        
        elif choice == "2":
            showTitle = input("Enter a title: ")

            print()

            showId = getShowId(showTitle)
            print("Show / Movie ID:" + showId)

            print()
            rating = scrapeShowRating(showId)
            print("Rating:", rating)

            print()
            showAbout = scrapeShowAbout(showId)
            print("About:", showAbout)

            print()
            creators = scrapeShowCreators(showId)
            print("Creators:")
            printAList(creators)

            print()
            castMembers = scrapeShowCast(showId)
            print("Cast members:")
            printAList(castMembers)

            print()
        
        elif choice == "0":
            print("Thank you for using IMDB Scraper.")
            break

        else:
            print("Invalid choice. Please enter a valid choice.")