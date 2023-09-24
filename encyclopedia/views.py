from django.shortcuts import render, redirect
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from markdown2 import Markdown
markdowner=Markdown()

class EntryForm(forms.Form):
    title=forms.CharField(label="Title",widget=forms.TextInput(attrs={'class':'form-control col-md-8 col-lg-8'}))
    content=forms.CharField(label="Content",widget=forms.TextInput(attrs={'class':'form-control col-md-8 col-lg-8', "rows":8}))
    edit=forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request, entry):
    entryPage=util.get_entry(entry)
    if entryPage is None:
        return render(request,"encyclopedia/error.html",{
            "title":entry,
            "message":"Page not found"
        })
    else:
        content=markdowner.convert(entryPage)
        return render(request,"encyclopedia/entry.html",{
            "content":content,
            "title":entry
            
        })

def search(request):
    data=request.GET.get("q","")
    if(util.get_entry(data) is not None):
        return HttpResponseRedirect(reverse('entry', kwargs={'entry': data}))
    else:
        subString=[]
        for entry in util.list_entries():
            if data.upper() in entry.upper():
                subString.append(entry)
        return render(request,"encyclopedia/index.html",{
            "entries": subString
        })
    
def create(request):
    if request.method=="POST":
        form=EntryForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            content=form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data['edit'] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('entry', kwargs={'entry':title}))
            else:
                return render(request,"encyclopedia/create.html",{
                    "present":True,
                    "form":form,
                    "entry":title
                })
        else:
            return render(request,"encyclopedia/error.html",{
                "message":"Form is not valid",
                "title":title
            })
    else:
        return render(request,"encyclopedia/create.html",{
            "form":EntryForm()
        })

def edit(request, entry):
    page=util.get_entry(entry)
    if page is None:
        return render(request,"encyclopedia/error.html",{
            "title":entry,
            "message": "Page not found"
        })
    else:
        form=EntryForm()
        form.fields['title'].initial=entry
        form.fields['title'].widget=forms.HiddenInput()
        form.fields['content'].initial=page
        form.fields['edit'].initial=True

        return render(request,"encyclopedia/create.html",{
            "form":form,
            "title":form.fields['title'].initial
        })
    
def randoms(request):
    entries=util.list_entries()
    num=len(entries)
    rand=random.randint(0, num-1)
    entry=entries[rand]
    return HttpResponseRedirect(reverse('entry', kwargs={'entry':entry}))