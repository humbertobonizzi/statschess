import requests
import os
import wget

#Formato de link para download dos arquivos
#https://theweekinchess.com/zips/twic1497g.zip
#https://theweekinchess.com/zips/twic920g.zip

for i in range(920, 1498):
    remote_url = f'https://theweekinchess.com/zips/twic1497g.zip'
    wget.download(remote_url)
    #local_file = f'twic{i}.zip'
    #data = requests.get(remote_url, allow_redirects=True)
    #with open(local_file, 'wb') as file:
    #    file.write(data.content)
    break


#remote_url = 'https://www.google.com/robots.txt'
# Define the local filename to save data
#local_file = 'local_copy.txt'
# Make http request for remote file data
#data = requests.get(remote_url)
# Save file data to local copy
#with open(local_file, 'wb')as file:
#file.write(data.content)
