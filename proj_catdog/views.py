'''This code handles rendering all html pages'''
import random
from django.shortcuts import render
from django.core.cache import cache
from . import breeds_work

def index(request):
    '''Function rendering index.html'''
    return render(request, "index.html")


def breeds_list(request):
    '''Function retrieving data via breeds_work.get_breeds_for_table to be 
    displayed and rendering breed_list.html'''
    breeds = breeds_work.get_breeds_for_table()
    return render(request, "breed_list.html", context={"breeds": breeds})


def add_breed(request):
    '''Function rendering breed_add.html'''
    return render(request, "breed_add.html")

def test_breed(request):
    '''Function randomly choosing questions for the test, writing them to file 
    via breeds_work.write_questions, and rendering index.html'''
    breed_dict = breeds_work.get_breeds_for_test()
    q1 = random.choice(list(breed_dict.keys()))
    breed_dict.pop(q1)
    q2 = random.choice(list(breed_dict.keys()))
    breed_dict.pop(q2)
    q3 = random.choice(list(breed_dict.keys()))
    breeds_work.write_questions([q1,q2,q3])
    return render(request, "test_breed.html", context={"quest_1": q1, "quest_2": q2, "quest_3": q3})

def send_test(request):
    '''Function handling test via POST request, analyzing the user input both
    by itself and via breeds_work.check_answers function. Provides all the 
    necessary information and renders test_request.html'''
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        test_answer_1 = request.POST.get("answer_1", "")
        test_answer_2 = request.POST.get("answer_2", "")
        test_answer_3 = request.POST.get("answer_3", "")
        context = {"user": user_name}
        context["useranswer1"] = test_answer_1
        if len(test_answer_1) == 0:
            context["isanswer1"] = False
            context["comment1"] = "Вы не ответили на первый вопрос"
        else:
            context["isanswer1"] = True
            context["comment1"] = "Ваш ответ на первый вопрос был принят"
        context["useranswer2"] = test_answer_2
        if len(test_answer_2) == 0:
            context["isanswer2"] = False
            context["comment2"] = "Вы не ответили на второй вопрос"
        else:
            context["isanswer2"] = True
            context["comment2"] = "Ваш ответ на второй вопрос был принят"
        context["useranswer3"] = test_answer_3
        if len(test_answer_3) == 0:
            context["isanswer3"] = False
            context["comment3"] = "Вы не ответили на третий вопрос"
        else:
            context["isanswer3"] = True
            context["comment3"] = "Ваш ответ на третий вопрос был принят"
        if (len(test_answer_1) == 0) and (len(test_answer_2) == 0) and (len(test_answer_3) == 0):
            context["success"] = False
            context["comment"] = "Вы не ответили ни на один вопрос"
        else:
            context["success"] = True
            context["comment"] = "Ваш тест принят"
        if context["success"]:
            context["success-title"] = ""
            grades = breeds_work.check_answers([test_answer_1, test_answer_2, test_answer_3])
            context["iscorrect1"] = grades[0]
            context["iscorrect2"] = grades[1]
            context["iscorrect3"] = grades[2]
            context["summary"] = sum(grades)
            context["max"] = len(grades)

            answers = breeds_work.get_answers()
            context["answer1"] = answers[0]
            context["answer2"] = answers[1]
            context["answer3"] = answers[2]
        return render(request, "test_request.html", context)

def send_breed(request):
    '''Function handling adding new breed to breeds.csv file via POST request, 
    analyzing, and writing to the file via breeds_work.write_breed function. 
    Provides all the necessary information and renders breed_request.html'''
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_breed = request.POST.get("new_breed", "")
        new_description = request.POST.get("new_description", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_description) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_breed) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            breeds_work.write_breed(new_breed, new_description)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "breed_request.html", context)

def show_stats(request):
    '''Function retrieving statistics via breeds_work.get_breeds_stats function
    and rendering stats.html'''
    stats = breeds_work.get_breeds_stats()
    return render(request, "stats.html", stats)
