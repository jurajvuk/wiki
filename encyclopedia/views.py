from django.shortcuts import render, redirect
from django import forms
from . import util
from markdown2 import Markdown

class NewPageForm(forms.Form):
    new_page_title = forms.CharField(label="Title")
    new_page_content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'rows':10, 'cols':150}))

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
        "title": title,
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
                "title": search,
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
    if request.method == "GET": 
        return render(request, "encyclopedia/new_page.html", {
            "form": NewPageForm()
        })
    else:
        title = request.POST.get('new_page_title')
        content = request.POST.get('new_page_content')
        check = util.get_entry(title)
        if not check:
            util.save_entry(title, content)
            return redirect('index')
        else:
            return render(request, "encyclopedia/new_page.html", {
            "form": NewPageForm(),
            "errorMessage": "There is already an entry with that title!"
            })

def edit(request, title):
    if request.method == "GET": 
        return render(request, "encyclopedia/edit.html", {
            "content": util.get_entry(title),
            "form": NewPageForm()  
        })
    