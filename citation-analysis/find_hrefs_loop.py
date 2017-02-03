'''
Right now, this builds a dictionary with domain names and the number of times each domain appears. I need to revise this
 so that it only looks for hrefs in the main text of the page. Right now, it's picking up share buttons and comments and
 all sorts of other stuff.
 The problem I'm having is searching for "a" tags in the results of a search for <div class="entry-content">
~~ I think I solved this problem. First, I do a find_all for div class entry-content. Then, I convert the results of
 that to a string. Then, I Soup that string, which lets me do another find_all for a.

'''

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

start_path = input('What is the start path?')

full_domains = {}

site_domains_w_page_details = {}
site_domains_unique = {}
site_domains_total = {}
page_domains = {}
all_site_domains_count = {}
all_site_domains_unique = []
all_site_domains = []
for path, subdirs, files in os.walk(start_path):
    for subdir in subdirs:
        for f in files:
            if f.endswith('.html'):
                file_errors = []
                file_path = path + '/' + f

                soup = BeautifulSoup(open(file_path, 'r'), 'lxml')

                content = soup.find_all('p')
                content = str(content)

                # The following couple of blocks (through the line that defines 'this_domain_name') identifies the domain of the page
                #  being scraped.
                this_domain_candidates = soup.find_all('meta', {'property': 'og:url'})
                t_d_candidates = []
                for can in this_domain_candidates:
                    a_domain = can.get('content')
                    #print(type(a_domain))
                    #print(a_domain)
                    t_d_candidates.append(a_domain)

                this_domain = []

                for f in t_d_candidates:
                    #print(type(f))
                    f_string = str(f)
                    if f_string.startswith('http'):
                        this_domain.append(f)
                if len(this_domain) == 1:
                    this_domain = this_domain[0]
                else:
                    print('More than one domain option \n')
                    for f in this_domain:
                        print(f)

                domain_parse = urlparse(this_domain)
                this_domain_name = domain_parse.netloc

                # This section searches for URLs in the main text of the page.
                soup = BeautifulSoup(content, 'lxml')
                main_text = soup.find_all('a')

                hrefs = []
                domains = []
                for link in main_text:
                    url = link.get('href')
                    url = str(url)
                    if url.startswith('http'):
                        hrefs.append(url)

                # This should build a list of unique domains in links in a page.
                all_domains = []
                for link in hrefs:
                    url_parts = urlparse(link)
                    domain = url_parts.netloc
                    all_domains.append(domain)
                    all_site_domains.append(domain)
                    if not domain in domains and not domain in this_domain_name:
                        domains.append(domain)
                    if not domain in all_site_domains_unique and not domain in this_domain_name:
                        all_site_domains_unique.append(domain)

                # This builds a dictionary with domain names associated with domain counts. When working across multiple
                #  pages, prob want another dictionary wrapped around this one for each page.
                domain_counts = {}
                for d in domains:
                    domain_count = 0
                    for y in all_domains:
                        if d == y:
                            domain_count +=1
                    domain_counts[d] = domain_count

            page_domains[file_path] = domain_counts
            site_domains_w_page_details[this_domain_name] = page_domains

        for d in all_site_domains_unique:
            site_domain_count = 0
            for y in all_site_domains:
                if d == y:
                    site_domain_count +=1
            all_site_domains_count[d] = site_domain_count

        site_domains_unique[this_domain_name] = all_site_domains_count
        site_domains_total[this_domain_name] = all_site_domains

    full_domains[this_domain_name] = site_domains_unique


'''
test = page_domains['http://www.totalsurvivalist.com/2016/11/realities-of-defensive-conflicts.html']

for domain in test:
    print(domain)
    print(type(test[domain]))


# I need to develop a count of unique domains found in a site, taking into account the total number of pages in the
#  site.
## Instead of doing this, add an additional dictionary above that compiles domains and domain counts (botn unique and
#  total counts) for the site, rather than for each page.
site_domains = {}
full_domain_list = []
overview_domain_list = []
for site in site_domains:
    #print(site)
    for page in site_domains[site]:
        #print(page)
        for domain in page_domains[page]:
            print(domain)
            if not domain in full_domain_list:
                full_domain_list.append(domain)
'''

end_on_comment = True
