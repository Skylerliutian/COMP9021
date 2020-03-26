import sys
import os
import re
import itertools
from pathlib import Path

def set_truth_table(sirs_name):
    number_of_sirs = len(sirs_name)
    possible_solu = list(itertools.product([0, 1], repeat=number_of_sirs))
    truth_table = []
    for i in range(len(possible_solu)):
        temp_dic = {}
        for j in range(number_of_sirs):
            temp_dic[sirs_name[j]] = possible_solu[i][j]
        truth_table.append(temp_dic)
    return truth_table
test_file = Path(input('Which text file do you want to use for the puzzle? '))

if not os.path.exists(test_file):
    print(f'There is no file named {test_file} in the working directory, giving up...')
    sys.exit()
with open(test_file, 'r') as file:
    content = file.read()
    content = content.replace('\n', ' ')
    content = content.replace('!"', '"!')
    content = content.replace('."', '".')
    content = content.replace('.', '. ')
    sentence_content = re.split(r'[.?!]', content)
    for i in range(len(sentence_content)):
        sentence_content[i] = sentence_content[i].strip()
    while '' in sentence_content:
        sentence_content.remove('')
    while ' ' in sentence_content:
        sentence_content.remove(' ')
    list_content = content.split(' ')
    for i in range(len(list_content)):
        list_content[i] = list_content[i].replace('!', '')
        list_content[i] = list_content[i].replace('?', '')
        list_content[i] = list_content[i].replace('"', '')
        list_content[i] = list_content[i].replace(',', '')
        list_content[i] = list_content[i].replace(':', '')
        list_content[i] = list_content[i].replace('.', '')
    while '' in list_content:
        list_content.remove('')
    while ' ' in list_content:
        list_content.remove(' ')
    capital_content = []
    for i in range(len(list_content)):
        if list_content[i].istitle():
            capital_content.append(list_content[i])
    normal_capital = ['Sir', 'Sirs', 'Knight', 'Knave', 'Knights', 'Knaves', 'I']
    sirs_name = []
    for i in range(len(sentence_content)):
        normal_capital.append((sentence_content[i].split())[0])
    for i in range(len(normal_capital)):
        normal_capital[i] = normal_capital[i].replace('!', '')
        normal_capital[i] = normal_capital[i].replace(',', '')
        normal_capital[i] = normal_capital[i].replace('.', '')
        normal_capital[i] = normal_capital[i].replace('"', '')
        normal_capital[i] = normal_capital[i].replace('?', '')
    for capital_word in capital_content:
        if capital_word not in normal_capital:
            sirs_name.append(capital_word)
    distinct_sirs_name = sorted(list(set(sirs_name)))
    print(f'The Sirs are: ', end='')
    for i in range(len(distinct_sirs_name) - 1):
        print(distinct_sirs_name[i],end=' ')
    print(distinct_sirs_name[-1])
    
    proof_1 = {}
    proof_2 = {}
    for i in range(len(sentence_content)):
        if '"' in sentence_content[i]:
            speaker_1 = re.findall(r'[\S\w\s]*\s\"', sentence_content[i])
            says = re.findall(r'\"[\w\s\S]*\S\"', sentence_content[i])
            speaker_2 = re.findall(r'\"\s[\w\s]*', sentence_content[i])
            str_says_1 = str(says).replace("['", '')
            str_says = str(str_says_1).replace("']", '')
            for people in distinct_sirs_name:
                if people in ''.join(speaker_1):
                    if people not in proof_1.keys():
                        proof_1[people] = []
                        proof_1[people].append(str_says)
                    else:
                        proof_1[people].append(str_says)
                elif people in ''.join(speaker_2):
                    if people not in proof_1.keys():
                        proof_1[people] = []
                        proof_1[people].append(str_says)
                    else:
                        proof_1[people].append(str_says)
    judge_table = set_truth_table(distinct_sirs_name)
    for people in proof_1.keys():
        for w in range(len(proof_1[people])):
            proof_2[people] = []
            str_proof_1_values = proof_1[people][w]
            for sir in distinct_sirs_name:
                if sir in str_proof_1_values:
                    proof_2[people].append(sir)
            if 'I ' in str_proof_1_values:
                proof_2[people].append(people)
            if ' us ' in str_proof_1_values:
                for sir in distinct_sirs_name:
                    proof_2[people].append(sir)
            if 'least one of' in str_proof_1_values and 'Knight' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s >= 1:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s == 0:
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'least one of' in str_proof_1_values and 'Knave' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s <= len(proof_2[people]) - 1:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s == len(proof_2[people]):
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'most one of' in str_proof_1_values and 'Knight' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s <= 1:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s > 1:
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'most one of' in str_proof_1_values and 'Knave' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s >= len(proof_2[people]) - 1:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s < len(proof_2[people]) - 1:
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'xactly one of' in str_proof_1_values and 'Knight' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s == 1:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s != 1:
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'xactly one of' in str_proof_1_values and 'Knave' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s == len(proof_2[people]) - 1:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s != len(proof_2[people]) - 1:
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'll of us' in str_proof_1_values and 'Knights' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    s = 0
                    if judge_table[i][people] == 1:
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s == len(proof_2[people]):
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s != len(proof_2[people]):
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'll of us' in str_proof_1_values and 'Knaves' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    s = 0
                    if judge_table[i][people] == 1:
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s == 0:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s != 0:
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'I am a Knight' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'I am a Knave' in str_proof_1_values:
                judge_table = []
                continue
            if 'Sir' in str_proof_1_values and 'or' in str_proof_1_values and 'is a Knight' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s >= 1:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s == 0:
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'Sir' in str_proof_1_values and 'or' in str_proof_1_values and 'is a Knave' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s <= len(proof_2[people]) - 1:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        s = 0
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s == len(proof_2[people]):
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'Sir' in str_proof_1_values and 'is a Knight' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        if judge_table[i][proof_2[people][0]] == 1:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        if judge_table[i][proof_2[people][0]] == 0:
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'Sir' in str_proof_1_values and 'is a Knave' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    if judge_table[i][people] == 1:
                        if judge_table[i][proof_2[people][0]] == 0:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        if judge_table[i][proof_2[people][0]] == 1:
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'are Knight' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    s = 0
                    if judge_table[i][people] == 1:
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s == len(proof_2[people]):
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s != len(proof_2[people]):
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
            if 'are Knave' in str_proof_1_values:
                comp_truth_table = []
                for i in range(len(judge_table)):
                    s = 0
                    if judge_table[i][people] == 1:
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s == 0:
                            comp_truth_table.append(judge_table[i])
                    if judge_table[i][people] == 0:
                        for name in proof_2[people]:
                            s += judge_table[i][name]
                        if s != 0:
                            comp_truth_table.append(judge_table[i])
                judge_table = comp_truth_table
                continue
    if len(judge_table) == 0:
        print('There is no solution.')
    if len(judge_table) > 1:
        print(f'There are {len(judge_table)} solutions.')
    if len(judge_table) == 1:
        print('There is a unique solution:')
        for sir in distinct_sirs_name:
            if judge_table[0][sir] == 1:
                judge_table[0][sir] = 'Knight'
            if judge_table[0][sir] == 0:
                judge_table[0][sir] = 'Knave'
        for sir in distinct_sirs_name:
            print(f'Sir {sir} is a {judge_table[0][sir]}.')
