from django.shortcuts import render, redirect
from markdown2 import Markdown
from django.http import Http404


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

def create(request):
    if request.method == "POST":
        create_title = request.POST["create_title"]
        create_content = request.POST["create_content"]
        titleCheck = util.get_entry(create_title)
        if titleCheck is not None:
            return render(request, "encyclopedia/error.html", {
                "error": "The title you want to create already exists."
            })
        else:
            util.save_entry(create_title, create_content)
            content_md = convert_md_to_html(create_title)
            return render(request, "encyclopedia/title.html", {
                "title": create_title,
                "content": content_md
            })
    else: #if it's a get method 
        return render(request, "encyclopedia/create.html")

def edit(request):
    if request.method == "POST":
        edit_title = request.POST["edit_title"]
        edit_content = util.get_entry(edit_title)
        return render(request, "encyclopedia/edit.html", {
            "title": edit_title,
            "content": edit_content
        })

def save(request):
    if request.method == "POST":
        edit_title = request.POST["edit_title"]
        edit_content = request.POST["edit_content"]
        util.save_entry(edit_title, edit_content)
        content_md = convert_md_to_html(edit_title)
        return render(request, "encyclopedia/title.html", {
            "title": edit_title,
            "content": content_md
        })
    else: #if it's a get method 
        raise Http404
