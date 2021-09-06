from django.http.response import JsonResponse
from django.shortcuts import render

import concurrent.futures

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("./file.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


# //////////////////////////////////// SCHEDULER////////////////////////////////////


# This  function is called from the setting.py file where the scheduler is run using thread. 
# This function will enable all the 'Mark as done' buttons on the habits bage
def enable_button():
    print("Hello")
    HabitscollRef = db.collection("Habits").stream()
    for habitDoc in HabitscollRef:
        habit_doc_data = habitDoc.to_dict()

        for i in range(len(habit_doc_data["items"])):
            print("Hello for loop")
            if habit_doc_data["items"][i]["done_today"]:
                habit_doc_data["items"][i]["done_today"] = False

        db.collection("Habits").document(
            habitDoc.id).set(habit_doc_data, merge=True)

# ///////////////////////////////////////////////////////////////////////////////////////////


# This takes the email and returns the doc_id(or say profile id of person from firestore database), from the profile collection
def getDocId(request):
    doc_id=None
    email = request.session["email"]
    docs_ref = db.collection("Profiles").where("email", "==", email).get()
    if docs_ref is not None:
        for doc in docs_ref:
            doc_id = doc.id
    return doc_id


# Returns all the habits of a person he has added
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
        habits_data_items = habits_data["items"]

    if request.method == "POST":
        habit_name = request.POST.get("habit_name")
        print(habit_name)
        data = {
            "habit_name": habit_name,
            "days_completed": 0,
            "done_today": False,
        }
        habit_name_list = []
        for ele in habits_data_items:
            habit_name_list.append(ele["habit_name"])

        last_added_habit = None
        try:
            last_added_habit = request.session["last_added_habit"]
        except:
            pass

        if habit_name not in ("", last_added_habit) and habit_name not in habit_name_list:

            request.session["last_added_habit"] = habit_name

            habits_data_items.append(data)
            if len(habits_data) == 0:
                habits_data["total_habits"] = 1
            else:
                print(habits_data)
                habits_data["total_habits"] = habits_data["total_habits"]+1
            habits_data["items"] = habits_data_items
            print(doc_id)

            db.collection("Habits").document(
                doc_id).set(habits_data, merge=True)

    print(habits_data)

    return render(request, "habits.html", context={"habits_data_items": habits_data_items})




# This function is called when the new habit is added.
def habits_ajax(request):
    # Getting the doc_id of user by email
    doc_id = getDocId(request)
    habits_data_items = []

    # Getting all habits
    habits_data = get_all_habits(doc_id)
    if habits_data is None:
        habits_data = {}
        habits_data_items = []
    else:
        habits_data_items = habits_data["items"]

    if request.method == "POST":
        # Getting the name of the requested habit/added habit
        habit_name = request.POST.get("habit_name")
        print(habit_name)

        # making data to be added to the database
        data = {
            "habit_name": habit_name,
            "days_completed": 0,
            "done_today": False,
        }
        habit_name_list = []
        for ele in habits_data_items:
            habit_name_list.append(ele["habit_name"])

        last_added_habit = None
        try:
            last_added_habit = request.session["last_added_habit"]
        except:
            pass

        # If the added habit is not empty or not the lastr added one and not already there only then add 
        if habit_name not in ("", last_added_habit) and habit_name not in habit_name_list:
            request.session["last_added_habit"] = habit_name

            habits_data_items.append(data)
            if len(habits_data) == 0:
                habits_data["total_habits"] = 1
            else:
                print(habits_data)
                # Increment the count after every habit is added
                habits_data["total_habits"] = habits_data["total_habits"]+1
            habits_data["items"] = habits_data_items
            print(doc_id)

            db.collection("Habits").document(
                doc_id).set(habits_data, merge=True)

    print(habits_data)

    context = {"habits_data_items": habits_data_items}
    return JsonResponse(context)



# This api is called when the user clicks on 'Mark as done button' in habits page.
def habit_days_completed_inc(request):
    print("\n\nhabit_days_completed")
    # Getting the doc_id of the loggedin user
    doc_id = getDocId(request)

    # Collecting the data of habit for which the button is pressed
    habit_name = request.POST["habit_name"]
    habits_data = get_all_habits(doc_id)
    habits_data_items = habits_data["items"]
    print(habits_data_items)

    # Getting the total number of habits he/she has added from database
    total_habits = habits_data["total_habits"]
    new_data = []

    # If some of the habits are already completed
    if "completed_habits" in habits_data.keys():
        completed_habits = habits_data["completed_habits"]
    else:
        completed_habits = []

    # Getting the particular habit from the array of all habits and then checking if the completed days
    # for this habit are equal to 25. If equal to 25 then move to completed habits and remove from the to be completed habits and decrement the total habits.
    # And increment the total_completed_habits.
    # Then push the data to the database 
    for i in range(0, total_habits):
        if habits_data_items[i]["habit_name"] == habit_name:
            habits_data["items"][i]["days_completed"] = habits_data["items"][i]["days_completed"]+1
            habits_data["items"][i]["done_today"] = True

            # remove the habit
            if habits_data["items"][i]["days_completed"] == 25:
                print("Hi")
                habits_data["total_habits"] = habits_data["total_habits"]-1
                completed_habits.append(habits_data["items"][i])
                if "total_completed_habits" in habits_data:
                    habits_data["total_completed_habits"] = habits_data["total_completed_habits"]+1
                else:
                    habits_data["total_completed_habits"] = 1
                continue
        new_data.append(habits_data["items"][i])

    habits_data["items"] = new_data
    habits_data["completed_habits"] = completed_habits

    db.collection("Habits").document(doc_id).set(habits_data, merge=True)

    return render(request, "habits.html", context={"habits_data_items": habits_data_items})
