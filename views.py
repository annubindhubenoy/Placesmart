from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import CustomUser



def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validation
        if not first_name or not last_name or not email or not password1 or not password2:
            messages.error(request, "All fields are required")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        # Create user
        user = CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1  # ⚠️ plain text, you may want to hash it later
        )

        # ✅ store user in session (instead of Django's login)
        request.session['user_id'] = user.id  

        return redirect('aptitudetest')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            username = CustomUser.objects.get(email=email).username
        except CustomUser.DoesNotExist:
            username = None

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('selection_page')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'login.html')


def home_view(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def aptitudetest_view(request):
    return render(request, 'aptitudetest.html')

def selection_page(request):
    return render(request, 'selection_page.html')

from django.http import HttpResponse  # ✅ Add this import
import pandas as pd  # Optional: move to top if not already

import pandas as pd
from django.shortcuts import render
import random

import pandas as pd
from django.shortcuts import render
import random

def ap_test1_view(request):
    # Load the question data
    df = pd.read_csv("final_questions_cleaned.csv", encoding='latin1')

    # Filter questions for specific subtopics (change IDs as needed)
    filtered_df = df[df['subtopic_id'].isin([1, 2])]

    # Split questions based on mark weightage
    one_mark_df = filtered_df[filtered_df['mark_weightage'] == 1]
    two_mark_df = filtered_df[filtered_df['mark_weightage'] == 2]

    # Randomly select 10 one-mark and 5 two-mark questions
    one_mark_sample = one_mark_df.sample(n=10, random_state=random.randint(1, 99999))
    two_mark_sample = two_mark_df.sample(n=5, random_state=random.randint(1, 99999))

    # Combine and shuffle the final question set
    final_questions = pd.concat([one_mark_sample, two_mark_sample]).sample(frac=1).reset_index(drop=True)

    # Rename option columns to match template
    final_questions = final_questions.rename(columns={
        "option1": "option_a",
        "option2": "option_b",
        "option3": "option_c",
        "option4": "option_d"
    })

    # Convert to list of dicts for rendering
    questions = final_questions.to_dict(orient='records')

    # Render the template
    return render(request, 'ap_test1.html', {'questions': questions})



import pandas as pd
from django.shortcuts import render
import random

def ap_test2_view(request):
    # Load CSV file
    df = pd.read_csv("final_questions_cleaned.csv", encoding='latin1')

    # Filter subtopics (adjust IDs if needed)
    filtered_df = df[df['subtopic_id'].isin([3, 4])]

    # Split based on mark weightage
    one_mark_df = filtered_df[filtered_df['mark_weightage'] == 1]
    two_mark_df = filtered_df[filtered_df['mark_weightage'] == 2]

    # Randomly select 10 one-mark and 5 two-mark questions
    one_mark_sample = one_mark_df.sample(n=10, random_state=random.randint(1, 99999))
    two_mark_sample = two_mark_df.sample(n=5, random_state=random.randint(1, 99999))

    # Combine and shuffle final questions
    final_questions = pd.concat([one_mark_sample, two_mark_sample]).sample(frac=1).reset_index(drop=True)

    # Rename columns for template compatibility
    final_questions = final_questions.rename(columns={
        "option1": "option_a",
        "option2": "option_b",
        "option3": "option_c",
        "option4": "option_d"
    })

    # Convert DataFrame to list of dictionaries
    questions = final_questions.to_dict(orient="records")

    # Render the template
    return render(request, "ap_test2.html", {"questions": questions})


def ap_test3_view(request):
    # Use 'latin1' encoding as specified in your original code
    try:
        df = pd.read_csv("final_questions_cleaned.csv", encoding='latin1')
    except FileNotFoundError:
        # Handle case where file is not found
        return render(request, "error_template.html", {"message": "Question file not found."})

    # --- 1. Filter by subtopic_id = 5 ---
    filtered_df = df[df['subtopic_id'] == 5]

    # --- 2. Separate by mark_weightage ---
    q_mark_2 = filtered_df[filtered_df['mark_weightage'] == 2]
    q_mark_1 = filtered_df[filtered_df['mark_weightage'] == 1]

    # --- 3. Sample Questions (5 x 2-mark, 10 x 1-mark) ---
    
    # Use random_state for reproducibility, and min() to prevent errors 
    # if there are fewer than the required number of questions.
    
    # 2-mark questions (Target: 5)
    num_2_mark = min(5, len(q_mark_2))
    # We use a fixed seed (42) for consistent random sampling for a specific test instance
    random_mark_2 = q_mark_2.sample(n=num_2_mark, random_state=42)

    # 1-mark questions (Target: 10)
    num_1_mark = min(10, len(q_mark_1))
    random_mark_1 = q_mark_1.sample(n=num_1_mark, random_state=42)

    # --- 4. Combine and Shuffle Questions ---
    
    # Concatenate the two samples
    random_rows = pd.concat([random_mark_2, random_mark_1])
    
    # Shuffle the combined DataFrame for a mixed order
    random_rows = random_rows.sample(frac=1, random_state=100).reset_index(drop=True) 
    
    # --- 5. Rename columns for the template ---
    random_rows = random_rows.rename(columns={
        "option1": "option_a",
        "option2": "option_b",
        "option3": "option_c",
        "option4": "option_d"
    })

    # --- 6. Pass data to the template ---
    return render(request, "ap_test3.html", {
        # 'orient="records"' converts the DataFrame to a list of dictionaries
        "questions": random_rows.to_dict(orient="records")
    })
def ap_test1_result(request):
    return render(request, 'ap_test1_result.html')

def ap_test2_result(request):
    return render(request, 'ap_test2_result.html')

def ap_test3_result(request):
    return render(request, 'ap_test3_result.html')



# Create your views here.
