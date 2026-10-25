from django.shortcuts import render, redirect
from .models import Topic,Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

def index(request):
    """学习笔记的主页。"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """显示所有的主题。"""
    # 改成只过滤当前登录用户的
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个主题机器所有条目"""
    topic = Topic.objects.get(id=topic_id)
    # 新增防盗检查
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """添加新主题。"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单。
        form = TopicForm()
    else:
        # POST提交的数据：对数据进行处理。
        form = TopicForm(data=request.POST)
        if form.is_valid():
            # 改成这三句
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # 显示空表单或指出表单数据无效。
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """在特定主题中添加新条目。"""
    topic = Topic.objects.get(id=topic_id)  # 先获取到对应的主题

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)  # 核心：先不存
            new_entry.topic = topic              # 绑上主题
            new_entry.save()                     # 再存进去
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request,  entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 新增防盗检查
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #初次请求:使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        #POST提交的数据：对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic':topic,'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)