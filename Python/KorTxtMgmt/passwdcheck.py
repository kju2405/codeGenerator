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
    if len(passwd) >= 15:                                                        # 길이 15 이상 여부
        lenCondition = 1
    
    return (numCondition + capCondition + smlCondition + spcCondition + lenCondition)

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