# 2022-1 경희대학교 캡스톤디자인1 프로젝트

<strong> 단어의 의미적 유사도를 응용한 암호 생성기 (Password generator with semantic similarity of words) </strong>

# 인원 구성
|구분|성명|학번|소속학과|학년|이메일|
|---|---|:-:|:-:|:-:|:-:|
|학생|최현호|2015104231|컴퓨터공학과|4|abs0lutezer0@khu.ac.kr |
|학생|김재웅|2018110648|컴퓨터공학과|4|kju2405@khu.ac.kr |

## 연구 목표
기존의 난수화 암호({W38sG~jQC_vX5hW[u 등)에 비해 외우기 쉬우면서도 보안성도 훌륭한 한글 자판 기반 암호를 생성합니다.

## 설치 방법
Git Clone을 통해 본 프로젝트 코드를 로컬에 저장합니다.
```git
git clone https://github.com/kju2405/codeGenerator.git
```

본 프로젝트는 Python `Flask` 환경에서 동작하며, 제대로 된 구동을 위해서는 `Word2Vec`의 설치 역시 필요합니다.

`Gensim` 라이브러리에 위치하고 있습니다.
```pip
pip install flask
pip install gensim
```

해당 프로젝트는 `./Web/src/app.py`를 빌드함으로써 작동시킬 수 있습니다.

## 디렉토리 명세
|디렉토리|설명|
|---|---|
|`./`|Git 구성요소 및 Word2Vec 모델 파일을 포함합니다.|
|`./Database/DB/`|데이터베이스 파일 및 DB 생성에 관여한 코드를 포함합니다. |
|`./Jupyter_Files/`|Word2Vec 학습 및 학습데이터 크롤링에 사용한 Jupyter Notebook 코드를 포함합니다.|
|`./NLP/`|Word2Vec 학습 완료된 모델의 성능을 검증하는 코드를 포함합니다.|
|`./Python/CrawlingWord/`|학습데이터 크롤링에 사용한 코드를 포함합니다.|
|`./Python/KorTxtMgmt/`|한글의 된소리화, 발음 기반 치환, 영문화, 암호 강도 점검 등에 사용한 코드를 포함합니다.|
|`./Reports/`|캡스톤디자인1 프로젝트 기초조사서, 중간보고서, 최종보고서, KCC2022 발표 논문을 포함합니다.|
|`./Unused/`|초기에 Github에 푸시하였으나, 용도폐기된 파일을 포함합니다.|
|`./Web/src/`|본 프로젝트를 구동하기 위한 Web 기반 코드를 포함합니다.|

## 프로그램 시연
![Final_gif](https://user-images.githubusercontent.com/95610222/172426420-d70be739-9c24-4d29-b28f-56313dd60655.gif)

자세한 프로젝트에 대한 명세는 `./Reports`의 pdf 파일을 참고하시길 바랍니다.
