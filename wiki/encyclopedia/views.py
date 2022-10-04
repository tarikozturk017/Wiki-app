from django.shortcuts import render
from markdown2 import Markdown
from django.http import Http404

from . import util


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


    
