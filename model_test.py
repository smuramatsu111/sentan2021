#検証用
import sentencepiece as spm

sp = spm.SentencePieceProcessor()
sp.Load("sentencepiece.model")

for i in sp.EncodeAsIds("織田信長は武将である。"):
    print(i, sp.IdToPiece(i))