'''
this is the main structure of a page 
https://www.dmgh.de/de/fs1/object/display/bsb00000449_00078
the diplomata start with page 78 which is noted as the last
number of the URL (without the styling stuff
I presume a width from page 78 to 602:
https://www.dmgh.de/de/fs1/object/display/bsb00000449_00602
overall 524 pages.
'''

import requests, time



def generateURLs(urlDmgh,pageLow,pageHigh):
	"""
	Given a base url, a start page number and
	an end page number, generate a list of urls.
	"""
	liste=[]
	for number in range(pageLow,pageHigh+1):
		url=urlDmgh+str(number)+'.html?html=true'
		liste.append(url)
	return liste

def getresponse(urlliste):
	"""
	Given a list of urls, return a list of responses.
	"""
	responselist=[]
	for url in urlliste:
		response=requests.get(url)
		responselist.append(response)
	return responselist

def getcontent(responses):
	"""
	Given a list of response objects, return their text
	content. The text needs to be encoded in utf-8 and
	non-200 responses are ignored.
	"""
	contentlist=[]
	for resp in responses:
		if resp.status_code == 200:
			resp.encoding = 'UTF-8'
			content= resp.text
			contentlist.append(content)
	return contentlist

def filtercontent(contentList):
	"""
	Given a list of string contents of web pages, filter
	out everything which is not in between a div with class
	'htmlText'. Return a list of filtered content.
	"""
	contents = []
	starttext = '<div class="htmlText">'
	endtext = '</div>'

	for content in contentList:
		startindex = content.find(starttext)
		if startindex is not -1:
			startindex += len(starttext)
			endindex = content.find(endtext, startindex)
			text = content[startindex:endindex]
			contents.append(text)
	return contents

def concatenate(contentList):
	return '\n'.join(contentList)


def writeToFile(contentstring, filename):
	with open(filename, 'w') as f:
		f.write(contentstring)
	print('file was written in',filename)


def test():
	"""Test allllll the functions. Just for quick displays"""
	# Teste `generateURLs()`
	test = generateURLs('https://www.dmgh.de/de/fs1/object/display/bsb00000449_',78,79)
	print(test)
	# Teste `getresponse()`
	ergebnis=getresponse(['https://www.dmgh.de/de/fs1/object/display/bsb00000449_78.html?html=true'])
	print(ergebnis)
	# Teste `getcontent()`
	content=getcontent(ergebnis)
	print(content)


def main():
	BASE_URL = 'https://www.dmgh.de/de/fs1/object/display/bsb00000449_'
	START_PAGE = 581
	END_PAGE = 602
	FILENAME = 'ddhiii'+ str(START_PAGE)+ '-' +str(END_PAGE)+ '.txt'


	start=time.time()
	urls = generateURLs(BASE_URL, START_PAGE, END_PAGE)
	responses = getresponse(urls)
	contents = getcontent(responses)
	only_ps = filtercontent(contents)
	one_batch = concatenate(only_ps)
	writeToFile(one_batch,FILENAME)
	end=time.time()
	print('Time: '+ str(end-start) + 'sec.')


if __name__=='__main__':
	# Either test....
	#test()
	# .... or run.
	main()
