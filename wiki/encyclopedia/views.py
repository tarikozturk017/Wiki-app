from django.shortcuts import render, redirect
from markdown2 import Markdown
from django.http import Http404
from django import forms
from django.urls import reverse


from . import util
#from wiki import encyclopedia

def convert_md_to_html(title):
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return Markdown().convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if title not in util.list_entries():
        raise Http404
    data = util.get_entry(title)
    print(title)
    print(Markdown().convert(data))
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "content": Markdown().convert(data)
    } )

def search(request):
    if request.method == "POST":
        search_input = request.POST['q'] # looks for name="q" in layout  
        html_content = convert_md_to_html(search_input) #md -> html 
        if html_content is not None:
            return render(request, "encyclopedia/title.html", {
                "title": search_input,
                "content": html_content
            })
        else:
            listEntries = util.list_entries()
            foundTitles = []
            for title in listEntries:
                if title.find(search_input) != -1:
                    foundTitles.append(title)
            return render(request, "encyclopedia/search.html", {
                "searches": foundTitles
            })
