from django.shortcuts import render, redirect
from user.models import User, Tag
from challenge.models import Challenge

# Create your views here.
def home(request):
    user=request.user
    if request.user.is_authenticated:
        try:
            tag = Tag.objects.get(user=user)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(user=user)
        tags = {
        'morning': tag.morning,
        'afternoon': tag.afternoon,
        'evening': tag.evening,
        'inside': tag.inside,
        'outside': tag.outside,
        'solo': tag.solo,
        'group': tag.group,
        'extreme': tag.extreme,
        'calm': tag.calm,
        'focus': tag.focus,
        'achievement': tag.achievement,
        'bodyhealth': tag.bodyhealth,
        'confidence': tag.confidence,
        'mental': tag.mental,
        'short': tag.short,
        'newtry': tag.newtry
        }
        tag_list=[]
        for tag_name, tag_value in tags.items():
            if tag_value is True:
                tag_list.append(tag_name)

        # challenges = Challenge.objects.filter(recommand__contains='싶어요')
        c1 = Challenge.objects.filter(title__contains='클라이밍')
        c2 = Challenge.objects.filter(sub_effect__contains='스트레스')
        challenges = c1.union(c2)

        # challenge = Challenge.objects.()
        return render(request, 'main/home.html', {'user':user, 'tag_list':tag_list, 'challenges':challenges})
    return render(request, 'main/splashscreen.html')
