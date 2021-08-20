import re

testFiles = ['A Deadly Vendetta-00.04.14.039-00.24.26.359-merged-00.00.20.000-01.20.14.048.mp4',
'Child 44-00.01.33.760-00.18.10.920-merged.mp4',
'Confessions of a Teenage Drama Queen-00.01.11.959-01.21.41.159.mp4',
'Devils\'s Knot-00.05.43.600-00.18.35.960-merged.mp4',
'Eight Below-00.02.25.280-01.51.51.239.mp4',
'Ella Enchanted-00.02.52.000-01.29.45.359.mp4',
'The Chronicles of Narnia The Lion, The Witch And The Wardrobe-00.01.02.000-02.07.06.199.mp4',
'The Damned United-00.03.53.919-01.32.43.039.mp4',
'The Peanut Butter Falcon-00.03.10.746-01.27.58.199.mp4',
'Nothing to change here.ts']

def main():

    searches = ['-\d{2}\.\d{2}\.\d{2}\.\d{3}','-merged']

    for f in testFiles:
        clean = f
        for search in searches:
            clean = replace(clean,search)

        print(clean)

def replace(text,pattern,replace=""):
    """Replaces the search term"""

    result = re.sub(pattern,replace,text)
    return result

if __name__ == "__main__":

    main()