# -*- coding: utf-8 -*-

# Copyright (C) 2012 emijrp <emijrp@gmail.com>
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

from bz2 import BZ2File
from wmf import dump
import re
import time
import sys
import wikipedia

def clean(s):
    s = re.sub(ur"\'{2,5}", ur"", s)
    return s

path = sys.argv[1]
if path.endswith('.bz2'):
    import bz2
    source = bz2.BZ2File(path)
elif path.endswith('.gz'):
    import gzip
    source = gzip.open(path)
elif path.endswith('.7z'):
    import subprocess
    source = subprocess.Popen('7za e -bd -so %s 2>/dev/null' % path, shell=True, stdout=subprocess.PIPE, bufsize=65535).stdout
else:
    # assume it's an uncompressed XML file
    source = open(self.filename)

dumpIterator = dump.Iterator(source)
t1 = time.time()
cpages = 0
crevs = 0
totalrevs = 0
for page in dumpIterator.readPages():
    #page.getId(), page.getTitle(), page.readRevisions()
    #rev.getId(), rev.getParentId(), rev.getTimestamp(), rev.getContributor(), rev.getMinor(), rev.getComment(), rev.getText(), rev.getSha1()
    for revision in page.readRevisions():
        revtext = revision.getText()
        m = re.findall(ur"(?im)==\s*Enlaces\s*externos\s*==", revtext)
        if m:
            #capturar enlaces externos
            ee = revtext.split(m[0])[1]
            m = re.findall(ur"(?im)\[\[\s*Categor", ee)
            if m:
                ee = ee.split(m[0])[0]
            enlaces = re.findall(ur"(?im)^\*\s*\[\s*(https?://[^\s\[\]\|]+?)[\s]([^\n\r\[\]\|]*?)\]", ee)
            if len(enlaces) < 10:
                continue
            
            #capturar enlaces a proyectos hermanos
            
            
            #capturar VT
            m = re.findall(ur"(?im)==\s*V[eé]ase\s*tambi[eé]n\s*==", revtext)
            if m:
                vt = revtext.split(m[0])[1]
                try:
                    vt = vt.split('==')[0]
                except:
                    pass
            sugerencias = re.findall(ur"(?im)^\*\s*\[\[([^\|\]\:]{3,30})\]\]", revtext)
            
            #capturar abstract
            
            #capturar la mejor imagen
            images = re.findall(ur"(?im)(?:Archivo|File|Image)\s*\:\s*([^\|\[\]]+?\.jpe?g)(?:\s*\|\s*(?:\d+px|thumb|thumbnail|frame|left|center|right)\s*)*?\|\s*([^\n\r]*?)\s*\]\]", revtext)
            image = ''
            imagedesc = ''
            for i, d in images:
                print i, d
                trozos = []
                for trozo in page.getTitle().split(' '):
                    if len(trozo) >= 3:
                        trozos.append(trozo)
                if trozos and re.search(ur"(?im)(%s)" % ('|'.join(trozos)), i):
                    image = i
                    imagedesc = d
            
            #salida
            print '-'*50
            print page.getId(), page.getTitle(), len(enlaces)
            print '-'*50
            
            resultados = u'\n'.join([u'{{Resultado\n|url=%s\n|relevancia=\n|título=%s\n|descripción=%s\n|actualización=\n}}' % (enlace, '', clean(desc)) for enlace, desc in enlaces])
            #resultados = u''
            output = u"""{{Infobox Resultado
|introducción=
|imagen=%s
|pie de imagen=%s
|wikipedia=%s
|sugerencias=%s
|resultados=%s
}}
""" % (image, imagedesc, page.getTitle(), ', '.join(sugerencias), resultados)
            if image:
                print output
            #p = wikipedia.Page(wikipedia.Site('todogratix', 'todogratix'), page.getTitle())
            #p.put(output, output)
            
            