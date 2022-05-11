#検証用
import sentencepiece as spm

sp = spm.SentencePieceProcessor()
sp.Load("sentencepiece.model")

for i in sp.EncodeAsIds("セネガル勝ってるよ"):
    print(i, sp.IdToPiece(i))