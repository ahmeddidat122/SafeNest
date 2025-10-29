from django.shortcuts import render

def design_home(request):
    """Design tools home page"""
    context = {
        'title': 'Design Tools',
    }
    return render(request, 'design/home.html', context)
