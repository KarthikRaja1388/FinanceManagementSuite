def get_admin_user(user):
    user_profile = user.profile
    if user_profile.user_type == 'ADM':
        account_admin = user
    else:
        account_admin = user_profile.account_owner
    return account_admin