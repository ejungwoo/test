import re

def extract_citations(file_name):
    with open(file_name, 'r') as file:
        contents = file.read()
        
    # Find all instances of \cite{...} in the contents
    citation_matches = re.findall(r'\\cite\{(.*?)\}', contents)
    
    # Split the comma-separated citations and add them to a set to eliminate duplicates
    citations = set()
    for match in citation_matches:
        citation_names = match.split(',')
        for citation_name in citation_names:
            citations.add(citation_name.strip())
    
    # Convert the set to a list and return it
    return list(citations)

citations = extract_citations('data/isoscaling.tex')
print(len(citations))
print(citations)

