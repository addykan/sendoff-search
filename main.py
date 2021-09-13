from dotenv import load_dotenv
import os, requests, json

load_dotenv()

dictKey = os.getenv('dictKey')

headers = {
    'x-rapidapi-key': os.getenv('x-rapidapi-key'),
    'x-rapidapi-host': os.getenv('x-rapidapi-host')
    }

def buildURL(word):
    baseURL = f'https://wordsapiv1.p.rapidapi.com/words/?partOfSpeech=adjective&letterPattern=^{word}'
    return baseURL

def myFilter(pred, L):
    if L == []: return []
    elif pred(L[0]):
        return [L[0]] + myFilter(pred, L[1:])
    else:
        return myFilter(pred, L[1:])

def getPossibleWords(letter, oldWords):
    url = buildURL(letter)
    response = requests.get(url, headers=headers)
    result = json.loads(response.text)
    return myFilter(lambda x: x not in oldWords, result['results']['data'])
    
def getDictWord(word, oldWords):
    candidates = getPossibleWords(word, oldWords)
    for i in range(len(candidates)):
        yield candidates[i]

def getDefinition(word):
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}'
    response = requests.get(url, headers=headers)
    result = json.loads(response.text)
    definitions = []
    results = result['results']
    for i in range(len(results)):
        definitions.append(results[i]['definition'])
    return definitions


def main():
    wordToCheck = "42"
    while (not wordToCheck.isalpha()):
        wordToCheck = input("Enter word prefix to search for: ")
    print(f"Checking word {wordToCheck}...")
    again = "Y"
    resultWords = set()
    result = getDictWord(wordToCheck, resultWords)
    while again.lower() == 'y':
        # resultWords.add(result)
        try:
            nextWord = next(result)
        except:
            print("No more words left")
            return
        print(f'Word: {nextWord}')
        print(f'Definition: {getDefinition(nextWord)}')
        again = input("Y/N to keep going: ")
        print("\n")
    return result

result = main()