import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    # Returns the probability  distribution over which a random surfer would next visit.
    linked_pages= list(corpus[page])

    dictionary = {page : (1-damping_factor) * (1/(len(linked_pages)+1)) for page,val in corpus.items()}

    if (len (linked_pages) == 0):
        for k,v in dictionary.items():
            dictionary[k]= (1/ len(corpus))
    else:
        for k in linked_pages:
                dictionary[k]= dictionary[k]+ (damping_factor * (1/len(linked_pages)))
    
    return (dictionary) 

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    # returns the estimated PageRank for each page in the corpus based on a sampling method
    page = random.choice (list(corpus.keys()))
    dic= {}
    for k,v in corpus.items():
        dic[k] = 0

    dic[page] = 1

    for x in range(1,n): 
        weight_model = transition_model(corpus, page, damping_factor)
        weight = []

        for x in sorted (list(weight_model.keys())):
            weight.append(weight_model[x])
        
        choice = random.choices(sorted(list(corpus.keys())), weight)[0]
        dic[choice] = dic[choice] + 1

        page = choice

    for k,v in dic.items():
        dic[k] = dic[k] / n
    return (dic)

    raise NotImplementedError

def linksTo (corpus, page):
    i = []
    for pages, links in corpus.items():
        if page in links:
            i.append(pages)
    return i

def iterate_pagerank(corpus, damping_factor):

    dic = {}
    N = len (corpus)

    for k,v in corpus.items():
        dic[k] = 1/ N
    
    threshold = list(dic.values())[0]
    error = 10

   
    while error > .001 : 
   

        pr = []

        for k in list (dic.keys()): 
            
            linked_to = linksTo(corpus, k)
            
            for each in linked_to:
             
                pr.append((dic[each] / len(list(corpus[each]))))
       
            dic[k] = damping_factor* sum(pr) + ((1-damping_factor) / N)
            pr.clear()

  
        error = abs (threshold - list(dic.values())[0])
        threshold = list(dic.values())[0]
       
    return (dic)

    raise NotImplementedError

if __name__ == "__main__":
    main()
