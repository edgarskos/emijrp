#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 emijrp
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import time
import urllib
import wikipedia

def unquote(s):
    s = re.sub(ur"&quot;", u'"', s)
    s = re.sub(ur"&#39;", u"'", s)
    s = re.sub(ur"\|", u"-", s)
    s = re.sub(ur'\\"', u'"', s)
    s = re.sub(ur'[\[\]]', u'', s)
    return s

ids = open('videoids.txt', 'r').read().splitlines()
for id in ids:
    url = 'http://www.youtube.com/watch?v=%s' % (id)
    f = urllib.urlopen(url)
    raw = unicode(f.read(), 'utf-8')
    f.close()
    
    try:
        title = re.findall(ur'<meta property="og:title" content="([^>]+?)">', raw)[0]
        title = unquote(title)
        os.system('python youtube-dl http://www.youtube.com/watch?v=%s --get-description > videodesc.txt' % (id))
        desc = unquote(unicode(open('videodesc.txt', 'r').read(), 'utf-8').strip())
        if desc == u'No description available.':
            desc = u''
        date = re.findall(ur'<span id="eow-date" class="watch-video-date" *?>([^>]+?)</span>', raw)[0]
        date = u'%s-%s-%s' % (date.split('/')[2], date.split('/')[1], date.split('/')[0])
        uploader = re.findall(ur'<link itemprop="url" href="http://www.youtube.com/user/([^>]+?)">', raw)[0]
        license = u'{{cc-by-3.0}}'
        if not re.search(ur"(?i)/t/creative_commons", raw):
            license = u'{{lye}}'
    except:
        print u'Error accediendo a los parámetros del vídeo', id
        g = open('errors.ids', 'a')
        g.write(u'%s\n' % (id))
        g.close()
        continue
        
    output = u"""{{Infobox Archivo
|embebido=YouTube
|embebido id=%s
|embebido usuario=%s
|embebido título=%s
|descripción=%s
|fecha de publicación=%s
|autor={{youtube channel|%s}}
|licencia=%s
}}
""" % (id, uploader, title, desc and u'{{descripción de youtube|1=%s}}' % (desc) or u'', date, uploader, license)
    
    p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), 'File:YouTube - %s - %s.jpg' % (uploader, id))
    if p.exists() and len(p.get()) < 10:
        print output
        p.put(output, u'BOT - Importando metadatos del vídeo de YouTube http://www.youtube.com/watch?v=%s' % (id))
        time.sleep(5)
