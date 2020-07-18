import json

#text = json.load( open('exemplo.json','r', encoding='utf-8'))

text2 = """{
   "result_index": 0,
   "results": [
      {
         "final": true,
         "alternatives": [
            {
               "transcript": "quem estÃ¡ no testamento ",
               "confidence": 0.82
            }
         ]
      }
   ]
}"""


print(json.loads(text2, encoding='utf-8')['results'][0 ]['alternatives'][0]['transcript'])