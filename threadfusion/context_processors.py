from .models import Profile, Question

def profile_context_processor(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    
    return {'profile_img': profile}