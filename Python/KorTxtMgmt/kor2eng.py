# Unicode based Kor to Eng
import sys

BASE_CODE = 44032                               # Unicode '가'
SET_AS_HEAD = 588                               # Unicode 초성화
SET_AS_BODY = 28                                # Unicode 중성화
END_OF_KOR = 55203                              # Unicode 한글 마지막


HEAD = list('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
BODY = list('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
TAIL = list(' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')

PLAIN_KOR = list('ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
STRONG_KOR = list('ㄲㄲㄳㄴㄵㄶㄸㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅆㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')

KOR = list('ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
ENG = ['r', 'R', 'rt', 's', 'sw', 'sg', 'e', 'E', 'f', 'fr', 'fa', 'fq', 'ft', 'fx', 'fv', 'fg', 'a', 'q', 
'Q', 'qt', 't','T', 'd', 'w', 'W', 'c', 'z', 'x', 'v', 'g','k', 'o', 'i', 'O', 'j', 'p', 'u', 'P', 'h', 'hk', 
'ho', 'hl', 'y', 'n', 'nj', 'np', 'nl', 'b', 'm', 'ml', 'l']

PRON = list('영공일원이둘투삼셋사넷포오육칠팔구비씨디지엘엠엔피큐알티유')
TRANS = ['0', '0', '1', '1', '2', '2', '2', '3', '3', '4', '4', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'g', 'l', 'm', 'n', 'p', 'q', 'r', 't', 'u']

def kor2pronkor(text):                                              # 발음 기반 숫자, 알파벳 변환
    result = ''
    for ch in text:
        if ch in PRON:
            for v in ch:
                if v != ' ':
                    result += ''.join(TRANS[PRON.index(v)])
        else:
            result += ch
    
    return result

def kor2eng(text):
    result = ''
    for ch in text:
        spl = split(ch)
        if spl is None:
            result += ch
        else:
            for v in spl:
                if v != ' ':
                    result += ''.join(ENG[KOR.index(v)])

    return result

def kor2strongkor(text):
    result = ''
    for ch in text:
        spl = split(ch)
        if spl is None:
            result += ch
        else:
            for v in spl:
                if v != ' ':
                    result += ''.join(STRONG_KOR[PLAIN_KOR.index(v)])
    
    return result

def combine(text):
    temp = []
    for v in text:
        temp.append(v)
    return korJoin(temp)

def korJoin(text):
    result = ""
    head, body, tail = 0, 0, 0
    text.insert(0, "")
    while len(text) > 1:
        if text[-1] in TAIL:
            if text[-2] in BODY:
                tail = TAIL.index(text.pop())
            else:
                result += text.pop()
        elif text[-1] in BODY:
            body = BODY.index(text.pop())
            head = HEAD.index(text.pop())
            result += chr(BASE_CODE + ((head * 21) + body) * SET_AS_BODY + tail)
            head, body, tail = 0, 0, 0
        else:
            result += text.pop()
    else:
        return result[::-1]


def split(kor):
    code = ord(kor) - BASE_CODE
    if code < 0 or code > END_OF_KOR - BASE_CODE:
        if kor == ' ': return None
        if kor in HEAD: return kor, ' ', ' '
        if kor in BODY: return ' ', kor, ' '
        if kor in TAIL: return ' ', ' ', kor
        return None
    return HEAD[code // SET_AS_HEAD], BODY[(code % SET_AS_HEAD) // SET_AS_BODY], TAIL[(code % SET_AS_HEAD) % SET_AS_BODY]

def main():
    print(split('뷁'))
    print(kor2strongkor("날시가 가다롭네요"))
    print(combine("ㄴㅏㄹㅆㅣㄲㅏ ㄲㅏㄸㅏㄹㅗㅂㄴㅔㅇㅛ"))
    textmessage = kor2pronkor('따이썬 다이팅')
    print(textmessage)
    print(kor2eng(kor2strongkor("날시가 가다롭네요")))
    print(kor2eng(textmessage))

if __name__ == '__main__':
    main()
