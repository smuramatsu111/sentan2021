import sentencepiece as spm

sp = spm.SentencePieceProcessor()
sp.Load("model/sentencepiece.model")

for i in sp.EncodeAsIds("セネガル勝ってるよ"):
    print(i, sp.IdToPiece(i))