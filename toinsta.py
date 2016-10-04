def sendstuff(filename, username, password):
       ''' I was using the handy 'Note In Reader' bookmarklet as my version of
           instapaper but Big G decided to remove this feature. So I had to go back
           to instapaper. 
           filename: The JSON file that can be downloaded from the export page at Reader.
           username & password: Instapaper username and password
        The code is very simple and assumes a lot of things going well. It does not
        handle the tag feature that was a part of Reader notes.
        ''' 
        import json
        from urllib2 import urlopen
        
        items = json.loads(file(filename).read()).values()[0]
        notsent = file('notsent.txt', 'w+')
        try:
                for item in items:
                        url = json.loads(urlopen(item['object']['url']).read())['items'][0]['alternate'][0]['href']

                        print url
                        urlopen('https://www.instapaper.com/api/add?username=' + 
                        username + '&password=' + password + '&url=' + url)
        except: 
                 notsent.write(url + '\n')
        notsent.close()
