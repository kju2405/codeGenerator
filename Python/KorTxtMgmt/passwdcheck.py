import re

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

    if len(passwd) >= 15:                                                       # 암호 길이 15 이상일 때
        if numCondition + capCondition + smlCondition + spcCondition < 3:       # 대소문자, 숫자, 특수기호 중 3가지 조건 이상 만족하는지 확인
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

def wordCheck(passwd):
    numCondition, capCondition, smlCondition, spcCondition = 0, 0, 0, 0
    if len(re.findall('[0-9]', passwd)) > 0:                                    # 숫자 포함 여부
        numCondition = 4
    if len(re.findall('[A-Z]', passwd)) > 0:                                    # 대문자 포함 여부
        capCondition = 2
    if len(re.findall('[a-z]', passwd)) > 0:                                    # 소문자 포함 여부
        smlCondition = 1
    if len(re.findall('[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', passwd)) > 0:     # 특수기호 포함 여부
        spcCondition = 8

    return numCondition + capCondition + smlCondition + spcCondition