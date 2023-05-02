def get_redirect_url(user):
    if user.role == 1:
        redirect_url='dashboardVendor'
    elif user.role ==2:
        redirect_url='dashboardCustomer'
    elif user.role is None:
        redirect_url='admin'
    return redirect_url    

