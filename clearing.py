'''
After requesting the files from dmgh
we should clear the files via regex from all 
tags we won't need. This includes p, i, span

An other task will be the separation of the diplomata
* Therefore we have to assemble all files into one text, *done*
* then separate them again by the number of the
    diplomata (by <p> xxx . </p> ) *done*
* create a dict for better operating *done*
* then use regex *done*
* get rid of the hyphenations *done*
'''

import re
from glob import glob


def collect_all_files(filepattern):
    '''
    with reading the folder from filepattern, def reads the names of the
    files and gives back a list of them. Plus should write a huge 
    single file where every content is included (in the right order)
    '''
    collecting_content=[]
    for filename in sorted(glob(filepattern)):
        with open(filename,'r', encoding='utf-8') as text:
            content = text.read()
            collecting_content.append(content)
    return ('\n').join(collecting_content)      


def separate(content):
    '''
    returns a list of all diplomata separated
    @<p> x.</p>. 
    x stands for the number of the diplomata
    plus: if there are several letters after the number
    of the diplomata ->(?:letter). 
    Eliminates the whitespace that is being created
    by the split function.
    '''
    reg_pattern = r'<p>(\s\d{1,3}\s(?:\s\w\s\s)?\.\s)</p>'
    diplomata = re.split(reg_pattern, content)
    diplomata = [elem for elem in diplomata if elem.strip()]
    
    return diplomata


def create_dict(diplomata):
    '''
    returns a dictionay via an iter funct. with the
    number of the diplomata : content of the diplomata
    as return value
    '''
    segments = {}

    for label,content in pairwise(diplomata):
        label = label.strip()
        segments[label] = content

    return segments


def clearing_tags(ordered_segments):
    '''
    recieves a dict with all diplomata and erases the 
    tags <p> <i> and <span> and closing tags.
    gives back a cleaned dict for further use
    new:19-04-19: also erases the following chars:
    #   * 
    #   ( )
    #   < > 
    #   every char from b - z 
    '''
    
    cleaned_dict={}
    cleanpattern= re.compile('<[^>]*>')
    #cleans alph and *. Replaced with whitespace 
    cleanpattern_alp=re.compile(r'\s[b-z\*]\s')
    #cleans parenthesis
    cleanpattern_par=re.compile(r'(\()|(\))')
    cleanpattern_tags=re.compile(r'(<)|(>)')

    for k,v in ordered_segments.items():
        v = re.sub(cleanpattern,'',v)
        v = re.sub(cleanpattern_alp,' ',v)
        v = re.sub(cleanpattern_par,'',v)
        v = re.sub(cleanpattern_tags,'',v)
        cleaned_dict[k] = v
    
    return cleaned_dict


def clearing_hyphemens(full_dict):
    '''
    recieves a dict and returns a dict, uses transform_
    content to get rid of all the unnecessary whitespaces
    '''
    final_dict = {}

    for label, content in full_dict.items():
        c = transform_content(content)
        final_dict[label] = c
    
    return final_dict

  
def transform_content(content):
    '''
    needs a string as input and gives back a string. 
    creates one big string. Clears all of the hyphenems in three cases:
     #1 combines all the words, that are pulled apart by the 
        html conversion
     #2 if inside the original artifact, a word is written apart, 
        the html marks this with '-' they also have to be corrected
     #3 all of the regular whitespaces that are set in the text (e.g.
        the two whitespaces between words)
    '''
    pattern_one = re.compile(r'( ){29}')
    pattern_hyphen = re.compile(r' -( ){27,28}')
    pattern_regular = re.compile(r'\s{2,28}')
    
    content = content.replace('\n', '')
    #1. case
    content = re.sub(pattern_one,'',content)
    #2. case
    content = re.sub(pattern_hyphen,'',content)
    # 3. case
    content = re.sub(pattern_regular, ' ', content)

    return content


def write_file(final_dict, results_dir='results/'):
    '''
    writes the file in a document called 'all diplomata.txt'
    '''
    content_string = ''
    for label, content in final_dict.items():
        content_string += label + '\n' + content + '\n\n'
        with open(results_dir + label+'.txt', 'w', encoding='utf-8') as d:
            d.write(content)
    with open(results_dir + 'all_diplomata.txt', 'w', encoding='utf-8') as c:
        c.write(content_string)



def pairwise(iterable):
    '''
    for creating the dictionary we iterate over the list
    and yielding them together in elem, content
    '''
    it=iter(iterable)

    if len(iterable) %2 !=0:
        raise ValueError("Contains more labels than diploma.")

    for elem in it:
        content = next(it)
        yield (elem, content)

        
if __name__ == '__main__':
    allfiles = collect_all_files('data/*.txt')
    diplomataList = separate(allfiles)
    dipldict = create_dict(diplomataList)
    final_diplomata = clearing_hyphemens(clearing_tags(dipldict))
    write_file(final_diplomata)

