from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown

class NewPageForm(forms.Form):
    new_page_title = forms.CharField(label="Title")
    new_page_content = forms.CharField(label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def content(request, title):
    content = util.get_entry(title)
    if content:
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
        "content": markdowner.convert(content),
    })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": "<p>Requested page was not found.</p>",
        })

def search(request):
    if request.method == "POST":
        search = request.POST.get("q")
        content = util.get_entry(search)
        if content:
            markdowner = Markdown()
            return render(request, "encyclopedia/entry.html", {
                "content": markdowner.convert(content),
            })
        else:
            all_entries = util.list_entries()
            search_string_length = len(search)
            substrings = []
            for entry in all_entries:
                if entry[:search_string_length].lower() == search.lower():
                    substrings.append(entry)
            return render(request, "encyclopedia/search.html", {
                "entries": substrings,
                "string_len": search_string_length,
                "search": search
            })

def create(request):
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })