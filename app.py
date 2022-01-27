import random
import json
from os import system as terminal
from platform import system as platform
import time
import os.path

class Colors: 
    BLACK = '\033[30m' 
    RED = '\033[31m' 
    GREEN = '\033[32m' 
    YELLOW = '\033[33m' 
    BLUE = '\033[34m' 
    MAGENTA = '\033[35m' 
    CYAN = '\033[36m' 
    WHITE = '\033[37m' 
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def sent(text, prefix=f"{Colors.WHITE}[{Colors.GREEN}*{Colors.WHITE}]{Colors.RESET} ", color=Colors.WHITE, bold=True, end="\n"):
    if bold:
        print(f"{prefix}{Colors.BOLD}{color}{text}{Colors.RESET}", end=end)
    else:
        print(prefix + color + text + Colors.RESET, end=end)

def clear():
    if platform()=='Windows':terminal('cls')
    else:terminal('clear')

def saveJsonFile(file, data: dict):
    with open(file, 'w', encoding='UTF-8-sig') as f:
        json.dump(data, f, indent=4, ensure_ascii = False)

def readJsonFile(file):
    with open(file, 'r', encoding='UTF-8-sig') as f:
        return json.load(f)

class EnglishApp:
    
    def add_word(self, filename):
        """
        영어단어 입력 방식:

        '[ Menu ]'
        > 영어단어
        > 뜻
        . . .
        > exit

        (!exit, !종료, !leave, !저장를 이용하여 종료 가능)
        """
        clear()
        print(f"{Colors.BOLD}{Colors.WHITE}[ {Colors.GREEN}영어 단어 추가 {Colors.WHITE}]{Colors.RESET}\n\n")
        sent("종료하고 싶으시면 '!exit' 또는 '!종료' 또는 '!leave' 또는 '!저장'을 입력하세요.\n\n", bold=False, color=Colors.CYAN)
        word_dict = {}
        while True:
            word = input(f"{Colors.BOLD}{Colors.GREEN}영어단어 {Colors.WHITE} > {Colors.RESET}{Colors.WHITE}{Colors.BOLD} ")
            if word == "!exit" or word == "!leave" or word == "!종료" or word=="!저장":
                try:
                    print(f"{Colors.BOLD}{Colors.WHITE}[ {Colors.GREEN}저장 중 ...{Colors.WHITE}]{Colors.RESET}")
                    time.sleep(1.3)
                    for key in list(word_dict.keys()):
                        if key=="" or key == " " or key==None:
                            del word_dict[key]
                    if len(word_dict) == 0: sent("추가할 단어가 없습니다. 다시 시도해주세요.", color=Colors.RED)
                    else:
                        if os.path.isfile(filename):
                            sent(f"이미 {filename} 파일이 존재합니다. 덮어쓰시겠습니까? (Y/N)", color=Colors.YELLOW)
                            check = input(f"{Colors.BOLD}{Colors.GREEN}YES{Colors.MAGENTA}/{Colors.RED}NO{Colors.WHITE}{Colors.BOLD} > ")
                            if check=="YES" or check=="y" or check=="Y":
                                saveJsonFile(filename, word_dict)
                                sent(f"성공적으로 영어 단어를 {filename}에 저장하였습니다.", color=Colors.GREEN, bold=True)        
                            else:
                                sent("취소하였습니다.", color=Colors.RED)
                    break

                except Exception as e:
                    print(f"{Colors.BOLD}{Colors.WHITE}[ {Colors.RED}저장하는 과정에서 오류가 났습니다. error code: {e}{Colors.WHITE}]{Colors.RESET}")
                    break

            elif word != None or word != "" or word != " " or len(word) != 0:
                word = word.lower()
                meaning = input(f"{Colors.BOLD}{Colors.GREEN}뜻 {Colors.WHITE} > {Colors.RESET}{Colors.WHITE}{Colors.BOLD} ")
                if ", " in meaning: meaning = meaning.split(", ")
                elif "," in meaning: meaning = meaning.split(",")
                else: meaning = [meaning]
                word_dict[word] = meaning
            
            else:
                sent("영어 단어를 인식할수 없습니다!", color=Colors.RED, bold=True); continue


    def exam_vocabulary(self, filename, mode="ko-kr"):
        data = readJsonFile(filename)
        
        # random_dict create
        if mode != "ko-kr" or mode=="en":
            test_dict = {}
            for key, value in data.items(): test_dict[", ".join(value)] = key
            all_english = test_dict
            random_dict = []
            for i in range(len(list(test_dict.keys()))): v = random.choice(list(test_dict.keys())); random_dict.append({v:test_dict[v]}); del test_dict[v]
        else:
            random_dict = []
            for i in range(len(list(data.keys()))): v = random.choice(list(data.keys())); random_dict.append({v:data[v]}); del data[v]
            # print(random_dict)
        
        # exam
        clear()
        print(f"{Colors.BOLD}{Colors.WHITE}[ {Colors.GREEN}{filename} 영어 시험 {Colors.WHITE}]{Colors.RESET}\n\n")
        sent("결과는 마지막에 출력됩니다. 중간에 종료하실려면 !exit, !leave를 입력해주세요.\n\n", bold=False, color=Colors.CYAN)
        correct_list = []
        wrong_list = []
        correct_emoji = f"{Colors.GREEN}✔{Colors.RESET}"
        wrong_emoji = f"{Colors.RED}✘{Colors.RESET}"
        for i in range(len(random_dict)):
            for key in list(random_dict[i].keys()):
                sent(key, color=Colors.YELLOW, end="")
                answer = input(f"{Colors.BOLD}{Colors.WHITE} > {Colors.RESET}{Colors.WHITE}{Colors.BOLD} ")
                check = ",".join(random_dict[i][key])
            if answer == check:
                sent(f"{Colors.GREEN}{correct_emoji}{Colors.RESET}", color=Colors.GREEN, end="\n\n")
                correct_list.append(key)
            else:
                sent(f"{Colors.RED}{wrong_emoji}{Colors.RESET}", color=Colors.RED, end="\n\n")
                wrong_list.append(key)
        
        # print result
        if len(wrong_list) <= 0: # 100점
            sent(f"{Colors.GREEN}정답율은 {Colors.BOLD}{Colors.GREEN}{round(len(correct_list)/len(random_dict)*100)}%{Colors.WHITE}입니다.{Colors.RESET}\n\n", color=Colors.GREEN, bold=True)
            exit()
        else:
            sent(f"{Colors.RED}정답율은 {Colors.BOLD}{Colors.RED}{round(len(correct_list)/len(random_dict)*100)}%{Colors.WHITE}입니다.{Colors.RESET}\n", color=Colors.RED, bold=True)
            sent(f"{Colors.RED}오답 단어는 다음과 같습니다.{Colors.RESET}", color=Colors.RED, bold=True)
            for i in range(len(wrong_list)): sent(f"{Colors.RED}{i+1}. {wrong_list[i]}", color=Colors.RED, bold=True)
            exit()


app = EnglishApp()