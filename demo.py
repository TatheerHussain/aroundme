import requests
import json
from data_seacher import *
import random

#question = input('qustion:')
#passage = input('passage:')
def qanet(question, passage):
        payload = {"question": question, "passage": passage}
        r = requests.post("http://140.115.54.90:8080/answer", data= json.dumps( payload ) , headers = {'content-type': 'application/json'} )
        answer = json.loads(r.text)['answer']
        return answer

def main():
        try:
                finder = Seacher()
                question = 'where is Guizikeng Hiking Trail' # an instance of question here 
                print(question)
                annoy_list = finder.searchArticle(question)
                article = random.choice(annoy_list)
                print(article['url'])
                print("QANet say:", qanet(question, article['content']))
        except TypeError:
                      print("Error")

main()

