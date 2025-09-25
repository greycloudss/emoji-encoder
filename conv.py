ZWSP="\u200b"
ZWNJ="\u200c"
ZWJ="\u200d"
WJ="\u2060"
SEP="\u2063"
ENC_MAP={"00":ZWSP,"01":ZWNJ,"10":ZWJ,"11":WJ}
DEC_MAP={v:k for k,v in ENC_MAP.items()}



def encode_emoji(emoji,text):
    b=text.encode("utf-8")
    n = len(b)
    
    bits = format(n,"032b")+"".join(format(x,"08b") for x in b)
    
    if len(bits)%2:
        bits+="0"
    
    payload="".join(ENC_MAP[bits[i:i+2]] for i in range(0,len(bits),2))
    return emoji+SEP+payload

def decode_emoji(s):
    i = s.rfind(SEP)
    
    if i==-1:
        return s,""
    
    payload="".join(ch for ch in s[i+1:] if ch in DEC_MAP)
    
    if not payload:
        return s[:i],""
    
    bits="".join(DEC_MAP[ch] for ch in payload)
    
    n = int(bits[:32],2)
    data_bits=bits[32:32+8*n]
    
    b = bytes(int(data_bits[i:i+8],2) for i in range(0,len(data_bits),8))
    
    return s[:i],b.decode("utf-8")


mode = int(input("1. encode\n2. decode\n>"))

answer = ""

emoticon = input("Input emoji: ")

if mode == 1:
    text = input("Input payload: ")
    answer = encode_emoji(emoticon, text)
if mode == 2:
    _, answer = decode_emoji(emoticon)

print(answer)

