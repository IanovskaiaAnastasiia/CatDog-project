'''This code handles all the data processing in proj_catdog such as reading from
and writing to files, calculating statictics, checking answers, etc.'''

def get_breeds_for_table():
    '''Function reading the breeds.csv file and outputting the contents to be
    displayed in a table'''
    breeds = []
    with open("./data/breeds.csv", "r", encoding="utf-8") as f:
        cnt = 1
        for line in f.readlines()[1:]:
            breed, description, source = line.split(";")
            breeds.append([cnt, breed, description])
            cnt += 1
    return breeds

def get_breeds_for_test():
    '''Function reading the breeds.csv file and outputting its contents as a
    dictionary'''
    breed_list = {}
    with open("./data/breeds.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            breed, description, source = line.split(";")
            breed_list[description] = breed
    return breed_list

def write_questions(quest_list):
    '''Function writing down the random selection of questions to questions.csv
    file in order to check the answers later'''
    with open("./data/questions.csv", "w", encoding="utf-8") as f:
        for question in quest_list:
            f.write(str(question))
            f.write(";")
        f.close()

def get_answers():
    '''Function retrieving answers to the test questions from the questions.csv
    and a dictionary provided by get_breed_for_test function'''
    answers = []
    breed_dict = get_breeds_for_test()
    with open("./data/questions.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[0:]:
            quests  = line.split(";")
            for quest in quests:
                if len(quest) != 0:
                    answers.append(breed_dict[quest])
    return answers

def check_answers(user_answers):
    '''Function analyzing user_answers by comparing it to the data provided by
    get_answers function. Outputs an array of binary data corresponding to the
    correctness of the answers to the questions (1 is correct and 0 is 
    incorrect)'''
    iscorrect = []
    true_answers = get_answers()
    for i in range(len(true_answers)):
        if str(user_answers[i]).strip().lower() == str(true_answers[i]).strip().lower():
            iscorrect.append(1)
        else:
            iscorrect.append(0)
    return iscorrect

def write_breed(new_breed, new_description):
    '''Function adding user-inputted breed with name new_breed and decription
    new_description and writing it down to breeds.csv file'''
    new_breed_line = f"{new_breed};{new_description};user"
    with open("./data/breeds.csv", "r", encoding="utf-8") as f:
        existing_breeds = [l.strip("\n") for l in f.readlines()]
        title = existing_breeds[0]
        old_breeds = existing_breeds[1:]
    breeds_sorted = old_breeds + [new_breed_line]
    breeds_sorted.sort()
    new_breeds = [title] + breeds_sorted
    with open("./data/breeds.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_breeds))


def get_breeds_stats():
    '''Function analyzing data from breeds.csv file and outputting the 
    resulting statistics'''
    db_breeds = 0
    user_breeds = 0
    defin_len = []
    with open("./data/breeds.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            breed, defin, added_by = line.split(";")
            words = defin.split()
            defin_len.append(len(words))
            if "user" in added_by:
                user_breeds += 1
            elif "db" in added_by:
                db_breeds += 1
    stats = {
        "breeds_all": db_breeds + user_breeds,
        "breeds_own": db_breeds,
        "breeds_added": user_breeds,
        "words_avg": sum(defin_len)/len(defin_len),
        "words_max": max(defin_len),
        "words_min": min(defin_len)
    }
    return stats
