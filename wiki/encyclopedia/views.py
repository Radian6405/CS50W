from django.http import HttpResponse
from django.shortcuts import render, redirect
import markdown2
import random

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
            "title": name
        })
    
    #exceptional cases
    return render(request, "encyclopedia/notfound.html")

def search(request):
    #checking for request method
    if request.method == "POST":
        data = request.POST.get("q")
        entry = util.get_entry(data)

        #to redirect to proper wiki page
        if entry != None:
            html = markdown2.markdown(entry)
            return render(request, "encyclopedia/wikipage.html", {
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

    #exceptional cases
    return render(request, "encyclopedia/notfound.html")

def add(request):
    #accepting the incoming response to add
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")

        #checking for duplicate entries
        if title in util.list_entries():
            return render(request, "encyclopedia/addpage.html", {
                "message": "Page Already Exists",
                "body": body
            }) 

        #writing new data 
        util.save_entry(title, body)

        return redirect(f"wiki/{title}")

    #Default Page
    return render(request, "encyclopedia/addpage.html", {
        "message": "",
        "body": ""
    })


def edit(request):
    #loading up edit page 
    if request.method == "POST":
        title = request.POST.get("title")
        body = util.get_entry(title)

        #loading with already available data
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "body": body
        })

    #exceptional cases
    return render(request, "encyclopedia/notfound.html")

def save(request):
    #saving the data from edit page
    if request.method == "POST":
        title = request.POST.get("title")
        new_body = request.POST.get("body")
        util.save_entry(title, new_body)

        return redirect(f"wiki/{title}")

    #exceptional cases
    return render(request, "encyclopedia/notfound.html")

def randomPage(request):
    entries = util.list_entries()
    title = random.choice(entries)

    return redirect(f"wiki/{title}")