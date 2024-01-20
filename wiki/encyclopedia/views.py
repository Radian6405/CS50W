from django.http import HttpResponse
from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    #to redirect to proper wiki page
    entry = util.get_entry(name)
    if entry != None:
        html = markdown2.markdown(entry)
        return render(request, f"encyclopedia/wikipage.html", {
            "html": html,
            "title": name.upper()
        })
    
    return render(request, "encyclopedia/notfound.html")

def search(request):
    #checking for request method
    if request.method == "POST":
        data = request.POST.get("q")
        entry = util.get_entry(data)

        #to redirect to proper wiki page
        if entry != None:
            html = markdown2.markdown(entry)
            return render(request, f"encyclopedia/wikipage.html", {
                "html": html,
                "title": data.upper()
            })
        
        #to find similar entries to search text
        entries = util.list_entries()
        similar_entries = []
        for i in entries:
            if i.lower().find(data) != -1:
                similar_entries.append(i)
    
        #rendering the similar text
        return render(request, "encyclopedia/index.html", {
            "entries": similar_entries
        })

    #if request is get
    return render(request, "encyclopedia/notfound.html")
        