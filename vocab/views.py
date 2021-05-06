from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, request
from django.db.models import Q
from .models import Vocab, Mean

def index(request):
    latest_vocab_list = Vocab.objects.order_by('-pub_date')[:5]
    context = {'latest_vocab_list': latest_vocab_list}
    return render(request, 'vocab/index.html', context)

def detail(request, vocab_id):
    word = Vocab.objects.get(pk=vocab_id)
    word_type = word.mean_set.get(pk=vocab_id).type
    word_mean = word.mean_set.get(pk=vocab_id).means_text
    vocab_detail = [{'vocab_text':word.vocab_text, 'vocab_type':word_type, 'vocab_mean':word_mean}]

    return render(request, 'vocab/detail.html', {
        'vocabulary': vocab_detail,
        'vocab': word
    })


def addvocab(request):
    if request.method == 'GET':
        return render(request, 'vocab/formadd.html')

    elif request.method == 'POST': # if submitted form
        word = request.POST.get('name').strip()
        word_type = request.POST.get('type').strip()
        meaning = request.POST.get('means').strip()

        if not Vocab.objects.filter(Q(vocab_text=word)).exists(): # if it is new word
            # create word and meaning
            create_word = Vocab(vocab_text=word)
            create_meaning = Mean(vocab=create_word, type=word_type, means_text=meaning)
            create_word.save()
            create_meaning.save()
            return HttpResponseRedirect('/vocab/')
        else:
            # if not new word
            existsWord = Vocab.objects.get(vocab_text=word) # get word

            if not Mean.objects.filter(Q(vocab=existsWord) & Q(means_text=meaning)).exists(): # if not have meaning of this vocab
                create_meaning = Mean(vocab=existsWord, type=word_type, means_text=meaning)
                create_meaning.save()
                return HttpResponseRedirect('/vocab/')
        
        return HttpResponseRedirect('/vocab/')