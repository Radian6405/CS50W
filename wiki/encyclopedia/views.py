from django.http import HttpResponse
from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    entry = util.get_entry(name)
    if entry != None:
        html = markdown2.markdown(entry)
        return render(request, f"encyclopedia/wikipage.html", {
            "html": html,
            "title": name.upper()
        })
    return render(request, "encyclopedia/notfound.html")