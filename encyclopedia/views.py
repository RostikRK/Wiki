from django.shortcuts import render, redirect
from django.http import Http404
from markdown2 import Markdown
from fuzzywuzzy import process
from random import randint

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    context = {}
    if title not in util.list_entries():
        raise Http404
    context["title"] = title
    context["content"] = Markdown().convert(util.get_entry(title))
    return render(request, 'encyclopedia/wiki.html', context)

def search(request):
    entry = request.POST["q"]
    if entry in util.list_entries():
        return redirect('encyclopedia:wiki', title=entry)
    else:
        context = {"title": entry}
        matches = process.extract(entry, util.list_entries())
        res = []
        for word in matches:
            if int(word[1]) > 70:
                res.append(word[0])
        context["entries"] = res
        return render(request, "encyclopedia/search.html", context)

def create(request):
    if request.method == "POST":
        context = {}
        title = request.POST["title"]
        if title in util.list_entries():
            raise Http404()
        content = request.POST["content-block"]
        util.save_entry(title, content)
        return redirect('encyclopedia:wiki', title=title)
    else:
        return render(request, "encyclopedia/create.html")

def edit(request, entry):
    if request.method == "POST":
        content = request.POST["content-block"]
        util.save_entry(entry, content)
        return redirect('encyclopedia:wiki', title=entry)
    else:
        context = {
            "title": entry,
            "content": util.get_entry(entry)}
        print(context["content"])
        return render(request, "encyclopedia/edit.html", context)

def random(request):
    the_index = randint(0, len(util.list_entries())-1)
    return redirect('encyclopedia:wiki', title=util.list_entries()[the_index])