#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import argparse

agent = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}

def get_price(card):
    req = requests.get('https://deckbox.org/mtg/' + card, headers=agent)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    prices = soup.find_all('div', class_='right price price_min')
    for price in prices:
        return price.text

def get_multi(card):
    multi = 1
    if card[0].isdigit():
        multi = ''
        for nr in card:
            if nr != 'x':
                multi += nr
            else:
                break
            
        card = card[len(multi)+1:]
        multi = int(multi)
        
    return card, multi


def main():
    parser = argparse.ArgumentParser(description =
                                     'Calculate the value your MTG deck')
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('-c', '--card', type=str,
                        help='Only search for one card', nargs='+')
    group.add_argument('-f', '--file', type=str,
                        help='Search for all the cards in a file')
    parser.add_argument('-v', '--verbose', action='count')

    args = parser.parse_args()
    
    if args.file:
        not_found = []
        total = 0
        f = open(args.file, 'r')
        
        for card in f:
            card = card.strip('\n')

            card, multi = get_multi(card)
            
            price = get_price(card)
            
            if price:
                price = float(price[2:])
                total += price * multi
                print('[+] {:<30}{:^.2f}${:>30.2f}$'.format(card, price, price*multi))
            else:
                print('[!] Got problem at card {}'.format(card))
                not_found.append(card)
                
        print('Total: {:.2f}$'.format(total))
        
        if len(not_found):
            text = 'The following cards couldn\'t be found: {}'.format(not_found[0])
            for i in range(1, len(not_found)):
                text += ', {}'.format(not_found[i])
            
            print(text)

        f.close()
        
    elif args.card:
        card = ''
        for word in args.card:
            card += word
            card += ' '

        card, multi = get_multi(card)
            
        price = get_price(card)
        price = float(price[2:])
        
        if price:
            print('[+] {:<30}{:^.2f}${:>30.2f}$'.format(card, price, price*multi))
        else:
            print('Card not found!')

    else:
        parser.print_help()

main()
