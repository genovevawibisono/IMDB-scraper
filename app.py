from bs4 import BeautifulSoup
import pandas as pd
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

    upcomingProjectsDiv = soup.find('div', id='accordion-item-actor-upcoming-projects').find('div', class_='ipc-accordion__item__content_inner accordion-content')
    if upcomingProjectsDiv:
        upcomingProjects = upcomingProjectsDiv.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between date-unrel-credits-list ipc-metadata-list--base')
        upcomingProjectsList = upcomingProjects.find_all('li', class_='ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-ee772624-0 eCnPST unreleased-credit')

        ActorUpcomingProjectsList = []

        for u in upcomingProjectsList:
            div = u.find('div', class_='ipc-metadata-list-summary-item__c').find('div', class_='ipc-metadata-list-summary-item__tc')
            title = div.find('a', class_='ipc-metadata-list-summary-item__t').get_text()

            ActorUpcomingProjectsList.append(title)
        
        return ActorUpcomingProjectsList
    
    return None

def printAList(l: list) -> None:
    for item in l:
        print(item)

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
        
        elif choice == "2":
            pass
        
        elif choice == "0":
            print("Thank you for using IMDB Scraper.")
            break

        else:
            print("Invalid choice. Please enter a valid choice.")