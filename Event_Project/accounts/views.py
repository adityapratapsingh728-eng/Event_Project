from django.shortcuts import render, redirect
from .models import CollegeData
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_str


def register_view(request):
    if request.method == "POST":
        f_name = request.POST.get('first_name','').strip()
        l_name = request.POST.get('last_name','').strip()
        username = request.POST.get('username')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')


        name = f"{f_name} {l_name}".strip()

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html')


        try:
            record = CollegeData.objects.get(college_id=username)
        except CollegeData.DoesNotExist:
            messages.error(request, "This ID is not registered with the college.")
            return render(request, "register.html")

        if record.name.lower() != name.lower():
            messages.error(request, "Name does not match college records.")
            return render(request, "register.html")

        if record.u_role != role:
            messages.error(request, "Role does not match college records.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "This account already exists.")
            return render(request, "register.html")
        
        user = User.objects.create_user(username=username, password=password, email=email ,first_name=f_name,last_name=l_name)
        group = Group.objects.get(name=role)
        user.groups.add(group)

        messages.success(request, "Registration successful!")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')

            elif user.groups.filter(name='Teacher').exists():
                return redirect('teacher_dashboard')

            elif user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')
            
            elif user.is_superuser:
                return redirect('/admin/')

        messages.error(request, "Invalid login")
    return render(request, "login.html")

def reset_pass(request):
    if request.method == "POST":
        f_name = request.POST.get('first_name').strip()
        l_name = request.POST.get('last_name').strip()
        username = request.POST.get('college_id').strip()
        email = request.POST.get('email').strip()
        
        try:
            user = User.objects.get(username=username, email=email, first_name =f_name, last_name=l_name)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_path = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_url = request.build_absolute_uri(reset_path)

            subject = "Password Reset Requested"
            message = f"Click the link to reset your password: {reset_url}"
            
            # FIX: Change 'admin@eventpro.com' to None to use your verified Brevo email
            send_mail(subject, message, None, [email])

            subject = "Password Reset Requested"
            message = f"Click the link to reset your password: {reset_url}"
            send_mail(subject, message, 'admin@eventpro.com', [email])

            messages.success(request, "Verification successful! Check your terminal for the link.")
            return render(request, "password_reset.html")

        except User.DoesNotExist:
            messages.error(request,"Identity verification failed. Details do not match.")
    return render(request,"password_reset.html")


def reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password reset successful! You can now login.")
                return redirect('login')
            else:
                return render(request,"reset_password.html", {"form": form, "validlink": True})
        else:
            form = SetPasswordForm(user)
        return render(request, "reset_password.html", {"form": form,"validlink" : True})
    else:
       return render(request, "reset_password.html", {"validlink": False})

def notification_main(request):
    events_list = [
        {'title': 'Annual Tech Symposium', 'details': 'A gathering of tech enthusiasts to discuss AI and future trends.'},
        {'title': 'Community Marathon', 'details': 'A 5k run starting at the city park to promote health and wellness.'},
        {'title': 'Local Art Showcase', 'details': 'Exhibition featuring paintings and sculptures from local artists.'},
        {'title': 'Luda', 'details': 'Exhibition featuring paintings and sculptures from local artists.'},
    ]
    return render(request, "notification_main.html", {'events': events_list})

def other_regis(request):
    return render(request,"other_regis.html")

def teacher_dashboard(request):
    return render(request,"teacher_dashboard.html")

def student_dashboard(request):
    return render(request,"student_dashboard.html")


def admin_dashboard(request):
    return render(request,"admin_dashboard.html")

def main_page(request):

    return render(request,"main.html")
