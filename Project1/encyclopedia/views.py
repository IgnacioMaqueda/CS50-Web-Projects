import random
from django.shortcuts import render, redirect
from django import forms
from . import util
from markdown import Markdown
from django.contrib import messages


class CreatePageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea())


class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())


def index(request):
    entries = util.list_entries()
    if request.method == "POST":
        title = request.POST.get('q')
        if title in entries:
            return redirect("wiki", title)
        return redirect("search", title)
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def wiki(request, title):
    markdowner = Markdown()
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "entry": markdowner.convert(entry)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })


def create(request):
    if request.method == "POST":
        form = CreatePageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                messages.error(request, "ERROR: Page already exists")
                return render(request, "encyclopedia/create.html", {
                    "form": form
                })
            else:
                util.save_entry(title, content)
                return wiki(request, title)
    else:
        return render(request, "encyclopedia/create.html", {
            "form": CreatePageForm()
        })


def randompage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return wiki(request, title)


def editpage(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            title = title
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return wiki(request, title)
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "form": EditPageForm(initial={'content': content}),
            "title": title,
            "content": content
        })


def search(request, title):
    entries = util.list_entries()
    entries = list(filter(lambda x: title in x, entries))
    return render(request, "encyclopedia/search.html", {
        "entries": entries
    })