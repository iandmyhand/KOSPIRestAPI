# KOSPIRestAPI

## Environments
- OS: Windows Server 2012 32Bit
    - Install Korean language pack.
    - Turn off firewall. (Manage it on AWS)
- Java: JDK1.8(32bit)
    - Tomcat8(32bit)
- Python: >= 3.5(32bit) [Anaconda](https://www.continuum.io/downloads)
- HTS: 
    - [eBest]()
        - Install AhnLab Safe Transaction on (http://cs.v3.co.kr)
            - Windows Server OS 설치 가능한 설치본 다운로드 (클릭) -> 설치하면 원격연결 안됨
    - [Daichin CYBOS Plus](http://www.daishin.co.kr/ctx_webservice/sc_download/sg_user_download/svc_download/download_main.html)
        - Turn off keyboard security.
- Editor: [Sublime Text 3](https://www.sublimetext.com/3)
    - install 'ConvertToUTF8' package for CJK encoding files.
- [Postman](https://www.getpostman.com/)

## Important!
#### Execute everything with Administration authority.

## Java

```
$ cd [PROJECT_ROOT]/java
$ gradle --info
```

## Python

```
$ cd [PROJECT_ROOT]/python
$ python server.py
```
