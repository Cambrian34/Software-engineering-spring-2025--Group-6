def activate_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        user.is_active = True
        user.save()

def setup_new_user(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and is_new:
        user.user_role = 'customer'
        user.is_active = True 
        user.save()