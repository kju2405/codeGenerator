import re
import kor2eng

def passwdCheck(passwd):
    numCondition, capCondition, smlCondition, spcCondition = 0, 0, 0, 0
    if len(re.findall('[0-9]', passwd)) > 0:                                    # 숫자 포함 여부
        numCondition = 1
    if len(re.findall('[A-Z]', passwd)) > 0:                                    # 대문자 포함 여부
        capCondition = 1
    if len(re.findall('[a-z]', passwd)) > 0:                                    # 소문자 포함 여부
        smlCondition = 1
    if len(re.findall('[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', passwd)) > 0:     # 특수기호 포함 여부
        spcCondition = 1

    if len(passwd) >= 15:                                                       # 암호 
        if numCondition + capCondition + smlCondition + spcCondition < 3:
            print(passwd)
            print(numCondition, capCondition, smlCondition, spcCondition)
            print("암호가 최소 요구사항을 만족하지 않습니다.")
            return False
        else:
            print(passwd)
            print(numCondition, capCondition, smlCondition, spcCondition)
            print("암호가 최소 요구사항을 만족합니다.")
            return True
    else:
        print("암호의 길이는 최소 15 이상이어야 합니다.")
        return False

text = '감자튀김삼성짜글이'
trans = kor2eng.kor2pronkor(text)
trans = kor2eng.kor2strongkor(trans)
result = kor2eng.kor2eng(trans)

passwdCheck(result)