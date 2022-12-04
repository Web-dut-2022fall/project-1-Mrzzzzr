# from cgitb import html
# from tkinter import E
# from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import markdown
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def getEntry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    else:
        return render(request, "encyclopedia/show.html", {
            "title": title,
            "entry": markdown.markdown(entry)
        })


def search(request):
    query = request.GET.get('q')
    entries = util.get_entry(query)
    if entries is None:
        return render(request, "encyclopedia/relate.html", {
            "entries": util.listRelateEntries(query)
        })
    else:
        return HttpResponse(markdown.markdown(entries))


def getRandomEntry(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return render(request, "encyclopedia/show.html", {
        "title": random_entry,
        "entry": markdown.markdown(util.get_entry(random_entry))
    })


def createPage(request):
    return render(request, "encyclopedia/create.html")


def createEntry(request):
    title = request.GET.get('title')
    content = request.GET.get('content')
    if util.get_entry(title) is None:
        util.save_entry(title, content)
        return render(request, "encyclopedia/show.html", {
            "title": title,
            "entry": markdown.markdown(content)
        })
    else:
        return HttpResponse("Entry already exists")


def editPage(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": markdown.markdown(entry)
        })


def editEntry(request):
    title = request.GET.get('title')
    content = request.GET.get('content')
    util.save_entry(title, content)
    return render(request, "encyclopedia/show.html", {
        "title": title,
        "entry": markdown.markdown(content)
    })
