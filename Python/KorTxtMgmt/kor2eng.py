# Unicode based Kor to Eng
import sys

BASE_CODE = 44032                               # Unicode '가'
SET_AS_HEAD = 588                               # Unicode 초성화
SET_AS_BODY = 28                                # Unicode 중성화
END_OF_KOR = 55203                              # Unicode 한글 마지막


HEAD = list('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')                               # 초성
BODY = list('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')                           # 중성
TAIL = list(' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')              # 종성

STRONG_KOR = list('ㄲㄲㄳㄴㄵㄶㄸㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅆㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')     # KOR list를 된소리화를 위해 ㄱ, ㄷ, ㅂ, ㅅ, ㅈ만 된소리로 변경

KOR = list('ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')            # 한글 목록
ENG = ['r', 'R', 'rt', 's', 'sw', 'sg', 'e', 'E', 'f', 'fr', 'fa', 'fq', 'ft', 'fx', 'fv', 'fg', 'a', 'q',                      # 쿼티 기반 알파벳
'Q', 'qt', 't','T', 'd', 'w', 'W', 'c', 'z', 'x', 'v', 'g','k', 'o', 'i', 'O', 'j', 'p', 'u', 'P', 'h', 'hk', 
'ho', 'hl', 'y', 'n', 'nj', 'np', 'nl', 'b', 'm', 'ml', 'l']

PRON = list('영공일원이둘투삼셋사넷포오육칠팔구비씨디지엘엠엔피큐알티유')                                                       # 문자 발음
TRANS = ['0', '0', '1', '1', '2', '2', '2', '3', '3', '4', '4', '4', '5',                                                       # 치환 숫자 및 알파벳 목록
        '6', '7', '8', '9', 'b', 'c', 'd', 'g', 'l', 'm', 'n', 'p', 'q', 'r', 't', 'u']

NUM_QWERTY = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']                                                                 # 쿼티 숫자 자판
CHAR_QWERTY = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']                                                                # 쿼티 숫자 자판 기반 특수기호

def kor2pronkor(text):                                                              # 발음 기반 숫자, 알파벳 치환
    result = ''
    for ch in text:
        if ch in PRON:                                                              # 낱말 단위로 PRON에 있을 경우 치환
            for v in ch:
                if v != ' ':
                    result += ''.join(TRANS[PRON.index(v)])
        else:
            result += ch                                                            # 없으면 그대로 저장
    
    return result

def num2shiftnum(text):                                                             # 쿼티 숫자를 특수기호로 치환
    result = ''
    for ch in text:
        if ch in NUM_QWERTY:                                                        # 낱말 단위로 NUM_QWERTY에 있을 경우 치환
            for v in ch:
                if v != ' ':
                    result += ''.join(CHAR_QWERTY[NUM_QWERTY.index(v)])
        else:
            result += ch                                                            # 없으면 그대로 저장
    
    return result

def kor2eng(text):
    result = ''
    for ch in text:
        spl = split(ch)                                                             # 초성, 중성, 종성으로 분할
        if spl is None:
            result += ch                                                            # 초성, 중성, 종성 다 아닐 경우(숫자, 알파벳, 공백 등)
        else:
            for v in spl:
                if v != ' ':
                    result += ''.join(ENG[KOR.index(v)])                            # 한글 자판 인덱스 기반 쿼티 자판으로 변경

    return result

def kor2strongkor(text):                                                            # 된소리화 (현재 초성 및 종성 모두 된소리화 되는 문제가 있음)
    result = ''
    for ch in text:
        spl = split(ch)
        if spl is None:
            result += ch
        else:
            for v in spl:
                if v != ' ':
                    result += ''.join(STRONG_KOR[KOR.index(v)])                     # 한글 자판 인덱스에서 된소리화 자판 인덱스로 변경 (ㄱ, ㄷ, ㅂ, ㅅ, ㅈ -> ㄲ, ㄸ, ㅃ, ㅆ, ㅉ)
    
    return result

def combine(text):                                                                  # String의 Array화
    temp = []
    for v in text:
        temp.append(v)
    return korJoin(temp)

def korJoin(text):
    result = ""
    head, body, tail = 0, 0, 0                                                      # 조립 시 배열의 인덱스 맞춤 용도
    text.insert(0, "")
    while len(text) > 1:                                                            # 조립 대상 배열의 끝까지 반복
        if text[-1] in TAIL:                                                        # 마지막 인덱스가 종성일 경우 (종성이 없는 조건 == 공백(스페이스바) 이기 때문에 종성 없는 문자 뒤에 공백이 오면 공백이 사라짐)
            if text[-2] in BODY:                                                    # 마지막에서 두 번째 인덱스가 중성일 경우 (중성은 무조건 모음)
                tail = TAIL.index(text.pop())                                       # 마지막 인덱스 추출해서 종성 파트에 삽입 (이후 text[-1] in tail 조건을 빠져나와 elif 조건에서 받침 있는 글자로 조합)
            else:
                result += text.pop()                                                # 중성이 없다 == 모음이 없다 == 자음 하나로만 이루어졌다 -> 자음만 추출해서 저장
        elif text[-1] in BODY:                                                      # 마지막 인덱스가 중성일 경우 (종성이 없는 한글 == '가' or '네'와 같은 받침 없는 글자)
            body = BODY.index(text.pop())                                           # 중성 저장
            head = HEAD.index(text.pop())                                           # 초성 저장
            result += chr(BASE_CODE + ((head * 21) + body) * SET_AS_BODY + tail)    # 초성, 중성, 종성 인덱스 확인하여 한 글자로 조합
            head, body, tail = 0, 0, 0                                              # 조합 끝났으니 초기화
        else:
            result += text.pop()                                                    # 한글이 아닌 경우 그냥 저장 (알파벳, 숫자, 특수기호)
    else:
        return result[::-1]                                                         # 역순으로 result에 저장했기 때문에 원래 읽혀야 하는대로 Return


def split(kor):
    code = ord(kor) - BASE_CODE                                                     # Unicode 기반으로 계산
    if code < 0 or code > END_OF_KOR - BASE_CODE:                                   # 초, 중, 종성이 결합된 형태의 문자가 아니라면 if 조건 진입
        if kor == ' ': return None
        if kor in HEAD: return kor, ' ', ' '
        if kor in BODY: return ' ', kor, ' '
        if kor in TAIL: return ' ', ' ', kor
        return None
    return HEAD[code // SET_AS_HEAD], BODY[(code % SET_AS_HEAD) // SET_AS_BODY], TAIL[(code % SET_AS_HEAD) % SET_AS_BODY]

def main():                                                                         # 테스트용 코드
    print(split('뷁'))
    print(kor2strongkor("날시각 가다롭네요".replace(" ", "")))
    print(combine("ㄴㅏㄹㅆㅣㄲㅏㄲ ㄲㅏㄸㅏㄹㅗㅂㄴㅔㅇㅛ".replace(" ", "")))
    textmessage = kor2pronkor('따이썬 다이팅')
    print(textmessage)
    print(kor2eng(kor2strongkor("날시가 가다롭네요")))
    print(kor2eng(textmessage))
    print(kor2eng("ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅇ").replace(" ", ""))
    print(num2shiftnum(textmessage))

if __name__ == '__main__':
    main()