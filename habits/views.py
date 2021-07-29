from django.http.response import JsonResponse
from django.shortcuts import render

import concurrent.futures

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate('./file.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()


# //////////////////////////////////// SCHEDULER////////////////////////////////////

def enable_button():
    print("Hello")
    HabitscollRef = db.collection("Habits").stream()
    for habitDoc in HabitscollRef:
        habit_doc_data = habitDoc.to_dict()

        for i in range(len(habit_doc_data['items'])):
            print("Hello for loop")
            if habit_doc_data['items'][i]['done_today']:
                habit_doc_data['items'][i]['done_today'] = False

        db.collection("Habits").document(
            habitDoc.id).set(habit_doc_data, merge=True)


# ///////////////////////////////////////////////////////////////////////////////////////////

def getDocId(request):
    email = request.session['email']
    docs_ref = db.collection('Profiles').where('email', '==', email).get()
    for doc in docs_ref:
        doc_id = doc.id
    return doc_id


# Returns all the habits of a person he has added currently
def get_all_habits(doc_id):
    doc_ref = db.collection("Habits").document(doc_id).get()
    habits_data = doc_ref.to_dict()  # All habits
    return habits_data


# Main function that renders the page
def habits(request):
    doc_id = getDocId(request)
    habits_data_items = []

    habits_data = get_all_habits(doc_id)
    if habits_data is None:
        habits_data = {}
        habits_data_items = []
    else:
        habits_data_items = habits_data['items']

    if request.method == 'POST':
        habit_name = request.POST.get('habit_name')
        print(habit_name)
        data = {
            "habit_name": habit_name,
            'days_completed': 0,
            "done_today": False,
        }
        habit_name_list = []
        for ele in habits_data_items:
            habit_name_list.append(ele['habit_name'])

        last_added_habit = None
        try:
            last_added_habit = request.session['last_added_habit']
        except:
            pass

        if habit_name not in ('', last_added_habit) and habit_name not in habit_name_list:

            request.session['last_added_habit'] = habit_name

            habits_data_items.append(data)
            if len(habits_data) == 0:
                habits_data['total_habits'] = 1
            else:
                print(habits_data)
                habits_data['total_habits'] = habits_data['total_habits']+1
            habits_data['items'] = habits_data_items
            print(doc_id)

            db.collection("Habits").document(
                doc_id).set(habits_data, merge=True)

    print(habits_data)

    return render(request, 'habits.html', context={'habits_data_items': habits_data_items})


def habits_ajax(request):
    doc_id = getDocId(request)
    habits_data_items = []

    habits_data = get_all_habits(doc_id)
    if habits_data is None:
        habits_data = {}
        habits_data_items = []
    else:
        habits_data_items = habits_data['items']

    if request.method == 'POST':
        habit_name = request.POST.get('habit_name')
        print(habit_name)
        data = {
            "habit_name": habit_name,
            'days_completed': 0,
            "done_today": False,
        }
        habit_name_list = []
        for ele in habits_data_items:
            habit_name_list.append(ele['habit_name'])

        last_added_habit = None
        try:
            last_added_habit = request.session['last_added_habit']
        except:
            pass

        if habit_name not in ('', last_added_habit) and habit_name not in habit_name_list:

            request.session['last_added_habit'] = habit_name

            habits_data_items.append(data)
            if len(habits_data) == 0:
                habits_data['total_habits'] = 1
            else:
                print(habits_data)
                habits_data['total_habits'] = habits_data['total_habits']+1
            habits_data['items'] = habits_data_items
            print(doc_id)

            db.collection("Habits").document(
                doc_id).set(habits_data, merge=True)

    print(habits_data)

    context = {'habits_data_items': habits_data_items}
    return JsonResponse(context)


def habit_days_completed_inc(request):
    print("\n\nhabit_days_completed")
    doc_id = getDocId(request)
    habit_name = request.POST['habit_name']
    habits_data = get_all_habits(doc_id)
    habits_data_items = habits_data['items']
    print(habits_data_items)
    # print(habits_data['total_habits'])

    total_habits = habits_data['total_habits']
    new_data = []

    if 'completed_habits' in habits_data.keys():
        completed_habits = habits_data['completed_habits']
    else:
        completed_habits = []

    for i in range(0, total_habits):
        if habits_data_items[i]['habit_name'] == habit_name:
            habits_data['items'][i]['days_completed'] = habits_data['items'][i]['days_completed']+1
            habits_data['items'][i]['done_today'] = True

            # remove the habit
            if habits_data['items'][i]['days_completed'] == 25:
                print("Hi")
                habits_data['total_habits'] = habits_data['total_habits']-1
                completed_habits.append(habits_data['items'][i])
                if 'total_completed_habits' in habits_data:
                    habits_data['total_completed_habits'] = habits_data['total_completed_habits']+1
                else:
                    habits_data['total_completed_habits'] = 1
                continue
        new_data.append(habits_data['items'][i])

    habits_data['items'] = new_data
    habits_data['completed_habits'] = completed_habits

    db.collection("Habits").document(doc_id).set(habits_data, merge=True)

    # print("============Hello=====================")
    return render(request, 'habits.html', context={'habits_data_items': habits_data_items})


# executor = concurrent.futures.ThreadPoolExecutor()

# def habit_days_completed_inc(request):
#     """
#     This function increments the days completed of the habit
#     """

#     return_val=None

#     future=executor.submit(habit_days_completed_inc_util,request)
#     return_val=future.result()
#     print(return_val)

#     return return_val