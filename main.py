import requests
from os import system
from time import sleep
from colorama import Fore

white = Fore.LIGHTWHITE_EX
correct = Fore.LIGHTGREEN_EX
false = Fore.LIGHTGREEN_EX
info = Fore.LIGHTCYAN_EX
question = Fore.LIGHTYELLOW_EX
l = Fore.LIGHTBLUE_EX


def clear():
    system('cls')

def title(http,https,socks5):
    system(f'title VALID HTTP: {http} / VALID HTTPS: {https} / VALID SOCKS5: {socks5}')

clear()

http_counter = 0
https_counter = 0
socks5_counter = 0

title(http_counter,https_counter,socks5_counter)

proxies = open('proxies.txt','r',encoding='utf-8').read().splitlines()
proxy_counter = len(proxies)

print(f'{question}[?] Do you want to save proxies in text file: (y/n)')

save_proxies = input('> ')

payload = {
    "type": 2,
    "timeout": 20,
    "publish": False,
    "proxies": proxies
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

url = 'https://checkerproxy.net/api/check'

req = requests.post(url=url,headers=headers,json=payload)
# i hope it's true, site written: 'The checking speed is about 1,000 units in 30 seconds.'
# edit: info is not correct :P
wait_time = (proxy_counter // 100 * 3) + 30
clear()
print(f'{info}[i] Please wait {wait_time} second.')
sleep(wait_time)
clear()
id = dict(req.json())['id']
print(f'{info}[i] Check Panel ---> https://checkerproxy.net/report/{id}\n')
result = requests.get(url = f'https://checkerproxy.net/api/report/{id}', headers=headers)
result = dict(result.json())['proxies']

for i in range(len(result)):
    proxy = result[i]['addr']
    proxy_type = result[i]['type']
    proxy_validity = 'TRUE'
    proxy_kind = result[i]['kind']
    proxy_addres = result[i]['addr_geo_country']
    proxy_ping = result[i]['timeout']
    
    if proxy_type == 2:
        proxy_type = 'HTTPS'
        https_counter += 1
        title(http_counter,https_counter,socks5_counter)
    elif proxy_type == 1:
        proxy_type = 'HTTP'
        http_counter += 1
        title(http_counter,https_counter,socks5_counter)
    elif proxy_type == 4:
        proxy_type = 'SOCKS5'
        socks5_counter += 1
        title(http_counter,https_counter,socks5_counter)
    elif proxy_type == 0 or proxy_type == None:
        proxy_validity = 'FALSE'
    
    if proxy_kind == 2:
        proxy_kind = 'ANONYMOUS'
    elif proxy_kind == 0:
        proxy_kind = 'TRANSPARENT'
    
    if proxy_addres == '':
        proxy_addres = 'NOT FOUND'
    if proxy_validity == 'TRUE':
        print(f'{correct}[+]{white} VALIDITY: {correct}{proxy_validity} {l}| {white}PROXY: {correct}{proxy} {l}| {white}TYPE: {correct}{proxy_type} {l}| {white}LOCATION: {correct}{proxy_addres} {l}| {white}KIND: {correct}{proxy_kind} {l}| {white}PING: {correct}{proxy_ping}ms')
    elif proxy_validity == 'FALSE':
        print(f'{false}[-]{white} VALIDITY: {false}{proxy_validity} {l}| {white}PROXY: {proxy}')
    
    if save_proxies == 'y':
        if proxy_validity == 'TRUE':
            if proxy_kind == 'ANONYMOUS':
                if proxy_type == 'HTTPS':
                    with open('Anonymous/https.txt','a',encoding='utf-8') as file:
                        file.write(f'{proxy}\n')
                elif proxy_type == 'HTTP':
                    with open('Anonymous/http.txt','a',encoding='utf-8') as file:
                        file.write(f'{proxy}\n')
                elif proxy_type == 'SOCKS5':
                    with open('Anonymous/socks5.txt','a',encoding='utf-8') as file:
                        file.write(f'{proxy}\n')
            elif proxy_kind == 'TRANSPARENT':
                if proxy_type == 'HTTPS':
                    with open('Transparent/https.txt','a',encoding='utf-8') as file:
                        file.write(f'{proxy}\n')
                elif proxy_type == 'HTTP':
                    with open('Transparent/http.txt','a',encoding='utf-8') as file:
                        file.write(f'{proxy}\n')
                elif proxy_type == 'SOCKS5':
                    with open('Transparent/socks5.txt','a',encoding='utf-8') as file:
                        file.write(f'{proxy}\n')
        elif proxy_validity == 'FALSE':
            with open('invalid.txt','a',encoding='utf-8') as file:
                file.write(f'{proxy}\n')

print(f'\n{correct}[+] Verification Successful!\n{info}[i] HTTP: {http_counter}\n[i] HTTPS: {https_counter}\n[i] SOCKS5: {socks5_counter}')
sleep(1.5)
print(f'\n{info}[i] You can close the program by pressing enter.')
input('')
