# -*- coding: utf-8 -*-

from re import findall
from re import sub

from os import walk
import os
import string
import urllib.request
from urllib.error import HTTPError



"""

"""
with open('mep_kontakt_sql_py3.dat', 'w') as fid:
    #Please set mypath to the downloaded folder! For example: mypath= '/home/lenovo/Desktop/CallforDemocracy/Mai_2016/www.europarl.europa.eu/meps/de/'
    mypath= ""
    f = []
    d = []
    name_list=[]
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        d.extend(dirnames)
        break
    counter=0
    

    for ordner in d:
        pfad = mypath + ordner + '/'
        for (dirpath, dirnames, filenames) in walk(pfad):
            for datei in filenames:
                if '_cv.html' in datei:
    
                    mep_name = datei.split('_cv.html')[0]
                    #print (mep_name)
                    name = sub('[_+]'," ",mep_name)
                    name = string.capwords(name)
                    
                    #special treatment of names with Mc
                    if 'Mc' in name:
                        #print( name)
                        name_copy = list(name)
                        for n in range(len(name)-1):                      
                            if (name[n]=='M' and name[n+1] == 'c'):
                                letter = name[n+2]
                                letter = letter.upper()
                                name_copy[n+2] = letter                                                    
                                name = ''.join(name_copy)
                    fid.write("""INSERT INTO Respondent (name, phone, email, url, nation, "group", party, committees, license, image) VALUES ('""")
                    name = sub("'","''",name) # Wichtig für SQL, da Hochkommas escaped werden müsssen
                    fid.write(name)
                    fid.write("','")
                    filepath = pfad + datei
                      
                    if os.path.exists(filepath):
                
                        with open(filepath, 'r') as html_file:
                            html = html_file.read()
                            ### searching telefon ###
                            telefon = findall('"phone">[0-9(+)\s]*', html)
        
                            if len(telefon) == 1:
                                telefon.append("no number available")
                                print(telefon)
                            tel_belgium = sub('[(]0[)]' , "", telefon[0])
                            tel_france  = sub('[(]0[)]' , "", telefon[1])                   
                            
                            tel_belgium = sub('[(+)]*[\s\s*]*["phone">]*' , "", tel_belgium)
                            tel_france  = sub('[(+)]*[\s\s*]*["phone">]*' , "", tel_france)
                            #print ("tel_belgium: ", tel_belgium, "tel_france; ", tel_france)
                            #print tel
                            fid.write(tel_belgium)
                            fid.write("','")
                            ### searching mail ###
                            mail = findall('href="mailto:[^ \t\n\r\f\v]+', html)
                            if len(mail) >= 1:
                                mail = sub('href="mailto:','', mail[0])
                                mail = sub('"','', mail)
                                mail = sub('[/[]dot]','.', mail)
                                mail = sub('[/[]at]','@', mail)
                                mail = mail[::-1]
                                #print(mail)
                            
                            
                                
                            else:
                                mail= ''
                            fid.write(mail)                       

                            fid.write("','") 
                            
                            ### searching for url ###
                            
                            url = findall('''href.+title="Webs''', html)
                            if len(url) >=1:
                                url = sub('href="','',url[0])
                                url = sub('"','',url)
                                url = sub(' title=Webs','',url)
                            else:
                                url= 'http://www.europarl.europa.eu/meps/de/'+ordner+'/'+datei

                            #print(url)
                            
                            url = sub("'","''",url) # Wichtig für SQL, da Hochkommas escaped werden müsssen

                            fid.write(url)                       
                            fid.write("','") 
                            
                            ### search for country ###
                            country = findall('nationality noflag".[^ \t\n\r\f\v]+', html)
                            country = sub('nationality noflag".','',country[0])
                            #print (country)
   
                            fid.write(country)
                            fid.write("','") 
                            
                            ### search for fraction ###[ \t\n\r\f\va-zA-Z0-9_]+
                            
                            fraction = findall('class="group [a-zA-Z0-9_]+..[^(<)]+', html)
                            fraction = sub('[\t\n\r\f\v]+', '', fraction[0])
                            fraction = sub('class="group[^(>)]+.', '', fraction)
                            
                            #print(fraction)
                            
                            fid.write(fraction)
                            fid.write("','") 
                            
                            
                            ### search for party ###
                            party = findall('name_pol_group".style."margin-left..0.".[^\t\n\r\f\v]+', html)
                            party = sub('name_pol_group".style."margin-left..0.".', '', party[0])
                            party = sub('..span.', '', party)
                            #print(party)
                            party = sub("'","''",party) # Wichtig für SQL, da Hochkommas escaped werden müsssen
                            fid.write(party)
                            fid.write("','") 


                            ### search for committees ###
                            
                            filepath_home = filepath[:-7] + 'home.html'
                            
                            with open(filepath_home, 'r') as html_file_home:
                                html_home = html_file_home.read()
                                committees = findall('acronym"[(>)][^(<)]+', html_home)
                                html_file_home.close()
                                committees = " ".join(committees)
                                committees = sub('acronym"[(>)]' , "", committees)
                            #print (committees)
                            fid.write(committees)
                            fid.write("','")
                            ### search for copyright ###
                            right = findall('copyright" content="[^(>)]+', html)
                            right = sub('copyright" content="','', right[0])
                            right = sub('" /','', right)
                            #print(right)

                            fid.write(right)
                            fid.write("','")

                            fotolink= 'http://www.europarl.europa.eu/mepphoto/' + ordner + '.jpg'

                            
                            fotoname=mep_name + '.jpg'
                            fotoname = sub("'", "", fotoname)
                            
                            fid.write(fotoname)
                            
                            try:
                                urllib.request.urlretrieve(fotolink, fotoname)
                            except HTTPError:
                                print('HTTPError')
                                print(fotoname)
                                print(fotolink)
                            
                            fid.write("');")


                            
                    fid.write('\n')
                    
fid.close()   









