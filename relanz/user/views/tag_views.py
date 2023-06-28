from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, UserTag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from config.email_decorator import email_verified_required
from django.db.models import Q, Count
from datetime import datetime

# @email_verified_required
@login_required(login_url='/user/signin')
def survey(request):
    if request.method=="GET":
        user = request.user
        return render(request, 'tag/survey.html', {user:user})
    if request.method=="POST":
        user=request.user
        if user.nickname is None:
            return redirect('user:content')
        if request.user.is_authenticated:
            # -------------------- 성별 기준 -------------------------
            sex_result_num = {
                '취약하지 않음': 0,
                '취약': 0,
                '매우 취약': 0,
            }
            user_sex = user.sex

            # 유저와 같은 성별인 데이터 필터링
            sex_group_users = User.objects.filter(
                Q(sex=user_sex)
            )

            for user in sex_group_users:
                if user.survey_result_count >= 1 and user.survey_result_count <= 3:
                    sex_result_num['취약하지 않음'] += 1
                elif user.survey_result_count >= 4 and user.survey_result_count <= 5:
                    sex_result_num['취약'] += 1
                elif user.survey_result_count >= 6 and user.survey_result_count <= 7:
                    sex_result_num['매우 취약'] += 1

            # -------------------- 나이 기준 -------------------------
            age_result_num = {
                '취약하지 않음': 0,
                '취약': 0,
                '매우 취약': 0
            }
            user_age = user.age

            # 유저 나이대 계산 (유저 나이가 23세면 20~29세)
            age_group_start = (user_age // 10) * 10
            age_group_end = age_group_start + 9

            # 유저와 같은 나이대인 데이터 필터링
            age_group_users = User.objects.filter(
                Q(birth__gt=datetime.now().year - age_group_end, 
                  birth__lt=datetime.now().year - age_group_start)
            )

            for user in age_group_users:
                if user.survey_result_count >= 1 and user.survey_result_count <= 3:
                    age_result_num['취약하지 않음'] += 1
                elif user.survey_result_count >= 4 and user.survey_result_count <= 5:
                    age_result_num['취약'] += 1
                elif user.survey_result_count >= 6 and user.survey_result_count <= 7:
                    age_result_num['매우 취약'] += 1

            # -------------------- 성별+나이 기준 ----------------------
            age_sex_result_num = {
                '취약하지 않음': 0,
                '취약': 0,
                '매우 취약': 0
            }
            
            # 유저와 같은 성별/나이대인 데이터 필터링 (20대 여성)
            age_sex_group_users = User.objects.filter(
                Q(sex=user_sex, 
                  birth__gt=datetime.now().year - age_group_end, 
                  birth__lt=datetime.now().year - age_group_start)
            )

            for user in age_sex_group_users:
                if user.survey_result_count >= 1 and user.survey_result_count <= 3:
                    age_sex_result_num['취약하지 않음'] += 1
                elif user.survey_result_count >= 4 and user.survey_result_count <= 5:
                    age_sex_result_num['취약'] += 1
                elif user.survey_result_count >= 6 and user.survey_result_count <= 7:
                    age_sex_result_num['매우 취약'] += 1
            

            # 인원수를 퍼센트로 계산
            total_sex_users = sex_group_users.count()
            total_age_users = age_group_users.count()
            total_age_sex_users = age_sex_group_users.count()

            sex_percentages = {key: round((value / total_sex_users) * 100) for key, value in sex_result_num.items()}
            age_percentages = {key: round((value / total_age_users) * 100) for key, value in age_result_num.items()}
            age_sex_percentages = {key: round((value / total_age_sex_users) * 100) for key, value in age_sex_result_num.items()}

            return redirect('user:tagsurvey')
    return render(request, 'main/home.html')

# @email_verified_required
@login_required(login_url='/user/signin')
def tagsurvey(request):
    if request.method=="GET":
        return render(request, 'tag/tagsurvey.html')
    if request.method=="POST":
        user=request.user
        if user.nickname is None:
            return redirect('user:content')
        try:
            tags = UserTag.objects.get(user=user)
        except UserTag.DoesNotExist:
            tags = UserTag.objects.create(user=user)
            return redirect('user:activetime')
        morning = request.POST.get('morning')
        afternoon = request.POST.get('afternoon')
        evening = request.POST.get('evening')
        inside = request.POST.get('inside')
        outside = request.POST.get('outside')
        solo = request.POST.get('solo')
        group = request.POST.get('Group')
        static = request.POST.get('static')
        dynamic = request.POST.get('dynamic')
        tags = UserTag.objects.get(user=user)
        tag_cnt = 0
        tag_lists = [morning, afternoon, evening, inside, outside, solo, group, static, dynamic]
        for tag_list in tag_lists:
            if tag_list is not None:
                tag_cnt += 1
        if tag_cnt > 0:
            if morning is not None:
                tags.morning = True
            if afternoon is not None:
                tags.afternoon = True
            if evening is not None:
                tags.evening = True
            if inside is not None:
                tags.inside = True
            if outside is not None:
                tags.outside = True
            if solo is not None:
                tags.solo = True
            if group is not None:
                tags.group = True
            if static is not None:
                tags.static = True
            if dynamic is not None:
                tags.dynamic = True
            tags.save()
            return redirect('user:avatar')
        else:
            messages.add_message(request, messages.ERROR, '')
            return render(request, 'tag/tagsurvey.html')
    return render(request, 'main/home.html')