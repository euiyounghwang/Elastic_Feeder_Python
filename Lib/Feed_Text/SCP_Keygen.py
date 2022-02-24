
import os

# file delete from the remote server
os.system('ssh tomadmt@127.0.0.1 -p22 "rm -rf /TOM/TEST/1.pptx"')


"""
[esuser@PLCFSERA1 ~]$ ssh tomadmt@127.0.0.1
The authenticity of host '127.0.0.1 (127.0.0.1)' can't be established.
RSA key fingerprint is SHA256:866XLEyRW8CgRxGsP0RQJJoQBL00Nf0uuqrWfJ/2wC8.
RSA key fingerprint is MD5:5b:3a:4c:ae:fe:7a:3e:fe:08:94:27:2a:e8:a7:a6:2e.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '127.0.0.1' (RSA) to the list of known hosts.
account@127.0.0.1's password: 
Last login: Mon Dec 14 09:58:34 2020 from 10.128.254.18
TLCFCON3:/TOM> exit
Connection to 127.0.0.1 closed.
[esuser@PLCFSERA1 ~]$ ssh-keygen -t rsa 
Generating public/private rsa key pair.
Enter file in which to save the key (/home/esuser/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/esuser/.ssh/id_rsa.
Your public key has been saved in /home/esuser/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:j6D7/hWyI2us4vG2R9fJYup7hQmL2OotB7Kp8N5UVGU esuser@PLCFSERA1
The key's randomart image is:
+---[RSA 2048]----+
|        ..E      |
|       . .       |
|      .          |
|     ..          |
|   o .ooS=..     |
|. o ooo.*==.     |
|.+.ooo.++oo      |
|+.+*o.=o.o       |
|o+==BO*+.        |
+----[SHA256]-----+
[esuser@PLCFSERA1 ~]$ 
[esuser@PLCFSERA1 ~]$ 
[esuser@PLCFSERA1 ~]$ ssh-copy-id tomadmt@127.0.0.1
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
tomadmt@10.132.12.90's password: 

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'account@127.0.0.1'"
and check to make sure that only the key(s) you wanted were added.

[esuser@PLCFSERA1 ~]$ 
[esuser@PLCFSERA1 ~]$ 
[esuser@PLCFSERA1 ~]$ ssh-copy-id account@127.0.0.1
[esuser@PLCFSERA1 ~]$ 
[esuser@PLCFSERA1 ~]$ scp account@127.0.0.1:/TOM/1.pptx /ES
1.pptx                                                                                                                                                                 100% 2972KB  19.2MB/s   00:00    
[esuser@PLCFSERA1 ~]$ cd /ES
[esuser@PLCFSERA1 ES]$ ls
1.pptx
[esuser@PLCFSERA1 ES]$ ls -al
total 2972
drwxr-xr-x   2 esuser esgrp      20 Dec 14 10:16 .
dr-xr-xr-x. 19 root   root      268 Nov 11 09:34 ..
-rw-r--r--   1 esuser esgrp 3043321 Dec 14 10:16 1.pptx
[esuser@PLCFSERA1 ES]$ 


#############################################################################
https://mytory.net/archives/1144

	
ssh를 이용한 파일 복사 scp 암호 없이 복사하는 방법도.

[2011년 8월 9일에 암호 없이 복사하는 방법을 추가했다. 그래서 재발행 - 녹풍]

일단 참고는 여기서 했다 : ssh를 이용한 파일 복사

간단한데, 일단 scp가 설치돼 있어야 한다. 리눅스는 쉬운데 윈도우는 어떻게 하는 모르겠다. 그래서 난 그냥 cygwin을 깔아서 했다.

명령어는 아래와 같다.

scp 계정ID@계정주소.com:/home/mytory/targetFile.zip /home/mytory/복사받을폴더

간단하다. 그러면 일단 암호를 물어보고 알아서 한다.

-r 옵션을 붙이면 하위 폴더를 포함해 디렉토리를 통째로 복사한다고 한다.

scp 계정ID@계정주소.com:/home/mytory/targetFolder /home/mytory/복사받을폴더

내 컴에서 원격으로 복사를 하는 것도 당연히 가능하다. 주소 형식을 맞추면 된다.
인증키를 사용해서 암호 입력을 생략하기

암호를 물어보는 과정을 거치지 않게 인증키를 사용하는 방법이 있다. 주의할 점은 authorized_keys는 폴더가 아니라 파일이라는 점이다. id_rsa.pub 안의 내용을 authorized_keys 파일에 붙여 넣으면 된다. 영어로 잘 나와 있는 설명은 SSHOpenSSHKeys 다.

나도 설명을 하겠다. 나는 영어 설명을 기준으로 한다.

일단 상황을 가정하자. 나는 Server 컴퓨터에서 Target 컴퓨터로 파일을 전송하는 스크립트를 만들려고 한다. Server에 있는 파일들을 백업한 다음 전송하는 스크립트다. (Target 컴퓨터의 IP는 192.168.0.100 이고, url은 mytarget.local 이라고 하자. 로그인 이름은 mytory다.)

이 경우 일단 Server 컴퓨터에서 다음 명령을 실행한다.

mkdir ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t rsa

.ssh 폴더에는 중요한 정보가 저장되므로 반드시 퍼미션을 700으로 해 줘야 한다.

ssh-keygen -t rsa 명령을 실행하면, 아래 질문들이 나오는데, 그냥 다 엔터치는 게 제일 속편하다.

Generating public/private rsa key pair.
Enter file in which to save the key (/home/b/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/b/.ssh/id_rsa.
Your public key has been saved in /home/b/.ssh/id_rsa.pub.

패스프레이즈는 암호키를 여는 암호인 듯하다. 이걸 입력해 주면 연결할 때 또 암호를 입력하게 되므로 그냥 아무것도 입력하지 않는다. 그러면 어떤 보안 문제가 생기는지는 잘 모르겠다.

여튼 다 엔터치고 나면 Server 컴퓨터에 개인키와 공개키가 생성된다. 그러면 이제 공개키를 Target 컴퓨터에 심어야 한다.

이를 위해 아래 명령어를 입력한다.

ssh-copy-id mytory@192.168.0.100

이렇게 하면 Target 컴퓨터의 /home/.ssh 폴더에 authorized_keys 라는 파일이 생기고 공개키가 복사된다.

이러면 모두 끝! 이제 Server 컴퓨터에서 Target 컴퓨터에 ssh 접속을 할 때나, scp 명령을 쓸 때나 암호를 묻지 않게 된다.
다른 방법 ? expect

다른 방법으로는 expect 라는 프로그램을 사용한 방법이 있다.
Buy me a coffee Buy me a coffee
?? [추천합니다] 필자가 촬영한 동영상 강의: 워드프레스로 개발하기 Part 1

- 이 포스트엔 댓글 기능이 없습니다. 댓글 대신 mail@mytory.net으로 메일 보내 주세요.
ⓒ 웹으로 말하기
mail@mytory.net Newsletter RSS Twitter Facebook Google+ GitHub
Powered By Jekyll

"""