#訓練用
import codecs
import re
import requests
from bs4 import BeautifulSoup

#コーパス作成
url = "https://ja.wikipedia.org/wiki/"
keyword_list = [
    "織田信長", "徳川家康", "豊臣秀吉",  
    "伊達政宗", "武田信玄", "上杉謙信",
    "明智光秀", "島津義弘", "北条氏康",
    "長宗我部元親", "毛利元就", "真田幸村",
    "立花宗茂", "石田三成", "浅井長政"
    
]

corpus = []
for keyword in keyword_list:
    # 戦国大名の記事をダウンロード
    response = requests.get(url + keyword)
    # htmlに変換
    html = response.text
    
    soup = BeautifulSoup(html, 'lxml')
    for p_tag in soup.find_all('p'):
        text = "".join(p_tag.text.strip().split(" "))
        if len(text) == 0:
            continue
        # e.g. [注釈9] -> ''
        text = re.sub(r"\[注釈[0-9]+\]", "", text)
        # e.g. [注9] -> ''
        text = re.sub(r"\[注[0-9]+\]", "", text)
        # e.g. [20] -> ''
        text = re.sub(r"\[[0-9]+\]", "", text)
        corpus.append(text)
        
print(*corpus, sep="\n", file=codecs.open("wiki.txt", "w", "utf-8"))


#モデルの学習
import sentencepiece as spm

spm.SentencePieceTrainer.Train(
    '--input=data/wiki.txt, --model_prefix=model/sentencepiece --character_coverage=0.9995 --vocab_size=8000 --pad_id=3'
)

#以下簡単な検証

sp = spm.SentencePieceProcessor()
sp.Load("model/sentencepiece.model")
print("70行目のテキスト：" + corpus[70]+"\n")

print("テキストを単語に分割")
print(sp.EncodeAsPieces(corpus[70]))
print("\n")

print("単語をテキストに分割")
print(sp.EncodeAsIds(corpus[70]))
print("\n")

print("単語列からテキストに変換")
tokens = ['松永久秀', 'らが', '共', '謀', 'して', '秀吉に', '敵対し', 'た', '。']
print(sp.DecodePieces(tokens))
print("\n")

"""

print("単語ID列からテキストに変換")
ids = sp.EncodeAsIds(corpus[70])
print(sp.DecodeIds(ids))

print("語彙数")
print(sp.GetPieceSize()) #len(sp)でも取得可能

print("単語ID")
print(sp.PieceToId('</s>'))#sp['</s>']でも取得可能

"""
