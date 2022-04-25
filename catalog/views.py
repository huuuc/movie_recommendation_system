from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from .models import User, Movie, UserTag, UserRate, WouldLikeList, HaveWatchedList, SearchHistory
from collections import defaultdict
import time
import json
from django.core import signing, serializers
import hashlib
from django.core.cache import cache

HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = 'WANG_SI_XU'
SALT = 'movie'
TIME_OUT = 30 * 60  # 30min


def encrypt(obj):
    """加密"""
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


def decrypt(src):
    """解密"""
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    return raw


def create_token(userid):
    """生成token信息"""
    # 1. 加密头信息
    header = encrypt(HEADER)
    # 2. 构造Payload
    payload = {"userid": userid, "iat": time.time()}
    payload = encrypt(payload)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    # 存储到缓存中
    cache.set(userid, token, TIME_OUT)
    return token


def get_payload(token):
    payload = str(token).split('.')[1]
    payload = decrypt(payload)
    return payload


# 通过token获取用户名
def get_userid(token):
    payload = get_payload(token)
    return payload['userid']
    pass


def check_token(token):
    if len(str(token).split('.')) != 3:
        return False
    userid = get_userid(token)
    last_token = cache.get(userid)
    if last_token:
        return last_token == token
    return False


def sign_in(request):
    account = request.POST.get('login_account')
    password = request.POST.get('login_password')
    if account is not None and password is not None:
        if account == '' or password == '':
            resp = {'err_msg': 'Account or password is empty'}
            return HttpResponse(json.dumps(resp), "application/json")
        user = User.objects.filter(account=account)
        if len(user) != 0 and user[0].password == password:
            token = create_token(user[0].id)
            return HttpResponse(token)
        else:
            resp = {'err_msg': 'Incorrect username or password'}
            return HttpResponse(json.dumps(resp), "application/json")
    resp = {'err_msg': 'can not find account or password'}
    return HttpResponse(json.dumps(resp), "application/json")


def sign_up(request):
    account = request.POST.get('reg_account')
    password = request.POST.get('reg_password')
    if account is not None and password is not None:
        if account == '' or password == '':
            resp = {'err_msg': 'Account or password is empty'}
            return HttpResponse(json.dumps(resp), "application/json")
        user = User.objects.filter(account=account)
        if len(user) != 0:
            resp = {'err_msg': 'The account has exist!'}
            return HttpResponse(json.dumps(resp), "application/json")
        user = User()
        user.account = account
        user.password = password
        try:
            user.save()
        except ValueError as err:
            resp = {'err_msg': err}
            return HttpResponse(json.dumps(resp), "application/json")
        token = create_token(user.id)
        return HttpResponse(token)
    resp = {'err_msg': 'can not find account or password'}
    return HttpResponse(json.dumps(resp), "application/json")


def get_type_list(request):
    param = json.loads(request.body)
    type_ = param.get('type')
    country = param.get('country')
    context = param.get('context')
    offset = param.get('offset')
    count = param.get('count')
    if type_ is None or country is None or context is None or offset is None or count is None:
        resp = {'err_msg': 'parameter invalid1'}
        print(request.body)
        return HttpResponse(json.dumps(resp), "application/json")
    offset = int(offset)
    count = int(count)
    if offset < 0 or count < 0:
        resp = {'err_msg': 'parameter invalid2'}
        return HttpResponse(json.dumps(resp), "application/json")
    # get overall list
    if type_ == '':
        movies = Movie.objects.all().order_by('-implicit_score')
    else:
        movies = Movie.objects.filter(type__contains=type_).order_by('-implicit_score')
    if country != '':
        movies = movies.filter(country__contains=country)
    if context != '':
        movies = movies.filter(name__contains=context)
    # 获取电影总数
    sum_movie = len(movies)
    paginator = Paginator(movies, count)
    try:
        movies = paginator.page(offset)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    except InvalidPage:
        # request offset not exist
        resp = {'err_msg': 'request page not exist'}
        return HttpResponse(json.dumps(resp), "application/json")
    tmp_resp = serializers.serialize("json", movies)
    resp = {'total': sum_movie, 'data': json.loads(tmp_resp)}
    return HttpResponse(json.dumps(resp), "application/json")


def get_movie_detail(request):
    movie_id = int(request.GET.get('movie_id'))
    if movie_id < 0:
        return render(request, '', {'err_msg': 'movie id not invalid'})
    movie_detail = Movie.objects.filter(movie_id=movie_id)
    if len(movie_detail) != 1:
        return render(request, '', {'err_msg': 'movie id not exist'})
    tags = UserTag.objects.filter(movie_id=movie_id)
    return render(request, '', {'movie_detail': movie_detail, 'comments': tags})


def rate_movie(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if check_token(token) is False:
        resp = {'err_msg': 'token check error'}
        return HttpResponse(json.dumps(resp), "application/json", status=400)
    user_id = get_userid(token)
    movie_id = int(request.POST.get('movie_id'))
    rating = int(request.POST.get('rate'))
    movie = Movie.objects.filter(movie_id=movie_id)
    user = User.objects.filter(id=user_id)
    if len(movie) != 1 or len(user) != 1:
        resp = {'err_msg': 'movie or user not exist'}
        return HttpResponse(json.dumps(resp), "application/json")
    old_record = UserRate.objects.filter(user=user[0], movie=movie[0])
    if len(old_record) != 0:
        resp = {'err_msg': 'rating record has existed'}
        return HttpResponse(json.dumps(resp), "application/json")
    record = UserRate()
    record.user = user[0]
    record.movie = movie[0]
    record.rate = rating
    try:
        record.save()
    except ValueError as err:
        resp = {'err_msg': err}
        return HttpResponse(json.dumps(resp), "application/json")
    movie[0].rate_num += 1
    rate_num = float(movie[0].rate_num)
    score = float(movie[0].score)
    movie[0].score = (score * (rate_num - 1) + 2 * rating) / rate_num
    movie[0].implicit_score = (rate_num / (rate_num + 1300)) * score + (1300 / (rate_num + 1300)) * 6.7
    try:
        movie[0].save()
    except ValueError as err:
        resp = {'err_msg': err}
        return HttpResponse(json.dumps(resp), "application/json")
    return HttpResponse()


def comment_movie(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if check_token(token) is False:
        resp = {'err_msg': 'token check error'}
        return HttpResponse(json.dumps(resp), "application/json", status=400)
    user_id = get_userid(token)
    movie_id = int(request.POST.get('movie_id'))
    comment = request.POST.get('comment')
    movie = Movie.objects.filter(movie_id=movie_id)
    user = User.objects.filter(id=user_id)
    if len(movie) != 1 or len(user) != 1:
        resp = {'err_msg': 'movie or user not exist'}
        return HttpResponse(json.dumps(resp), "application/json")
    record = UserTag()
    record.user = user[0]
    record.movie = movie[0]
    record.tag = comment
    try:
        record.save()
    except ValueError as err:
        resp = {'err_msg': err}
        return HttpResponse(json.dumps(resp), "application/json")
    return HttpResponse()


def add_would_like_movie(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if check_token(token) is False:
        resp = {'err_msg': 'token check error'}
        return HttpResponse(json.dumps(resp), "application/json", status=400)
    user_id = get_userid(token)
    movie_id = int(request.POST.get('movie_id'))
    movie = Movie.objects.filter(movie_id=movie_id)
    user = User.objects.filter(id=user_id)
    if len(movie) != 1 or len(user) != 1:
        resp = {'err_msg': 'movie or user not exist'}
        return HttpResponse(json.dumps(resp), "application/json")
    old_record = WouldLikeList.objects.filter(user=user[0], want_watch_movie=movie[0])
    if len(old_record) != 0:
        resp = {'err_msg': 'record has existed'}
        return HttpResponse(json.dumps(resp), "application/json")
    record = WouldLikeList()
    record.user = user[0]
    record.want_watch_movie = movie[0]
    try:
        record.save()
    except ValueError as err:
        resp = {'err_msg': err}
        return HttpResponse(json.dumps(resp), "application/json")
    return HttpResponse()


def add_have_watched_movie(request):
    movie_id = int(request.POST.get('movie_id'))
    user_id = int(request.POST.get('user_id'))
    movie = Movie.objects.filter(movie_id=movie_id)
    user = User.objects.filter(id=user_id)
    if len(movie) != 1 or len(user) != 1:
        return render(request, '', {'err_msg': 'movie or user not exist'})
    old_record = HaveWatchedList.objects.filter(user_id=user_id, have_watched_movie_id=movie_id)
    if len(old_record) != 0:
        return render(request, '', {'err_msg': 'record has existed'})
    record = HaveWatchedList()
    record.user = user[0]
    record.have_watched_movie = movie[0]
    try:
        record.save()
    except ValueError as err:
        return render(request, '', {'err_msg': err})
    return render(request, '')


def save_user_detail(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if check_token(token) is False:
        resp = {'err_msg': 'token check error'}
        return HttpResponse(json.dumps(resp), "application/json", status=400)
    user_id = get_userid(token)
    nick_name = request.POST.get('nick_name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    age = request.POST.get('age')
    sex = request.POST.get('sex')
    profession = request.POST.get('profession')
    user = User.objects.filter(id=user_id)
    if len(user) != 1:
        resp = {'err_msg': 'user not exist'}
        return HttpResponse(json.dumps(resp), "application/json")
    user[0].nick_name = nick_name
    user[0].phone = phone
    user[0].email = email
    if age != '':
        user[0].age = age
    user[0].sex = sex
    user[0].profession = profession
    try:
        user[0].save()
    except ValueError as err:
        resp = {'err_msg': str(err)}
        return HttpResponse(json.dumps(resp), "application/json")
    return HttpResponse()


def get_user_detail(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if check_token(token) is False:
        resp = {'err_msg': 'token check error'}
        return HttpResponse(serializers.serialize('json', resp), "application/json", status=400)
    user_id = get_userid(token)
    user = User.objects.filter(id=user_id)
    if len(user) != 1:
        return render(request, '', {'err_msg': 'user not exist'})
    context = {
        'nick_name': user[0].nick_name,
        'phone': user[0].phone,
        'email': user[0].email,
        'age': user[0].age,
        'sex': user[0].sex,
        'profession': user[0].profession,
        'account': user[0].account,
        'password': user[0].password
    }
    return HttpResponse(json.dumps(context), "application/json")


def get_movie_list(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if check_token(token) is False:
        resp = {'err_msg': 'token check error'}
        return HttpResponse(json.dumps(resp), "application/json", status=400)
    user_id = get_userid(token)
    param = json.loads(request.body)
    type_ = param.get('type')
    offset = param.get('offset')
    count = param.get('count')
    if type_ is None or offset is None or count is None:
        resp = {'err_msg': 'parameter invalid'}
        return HttpResponse(serializers.serialize('json', resp), "application/json")
    count = int(count)
    offset = int(offset)
    type_ = int(type_)    # 0: have_watched_list  1: would_like_list
    if offset < 0 or count < 0 or type_ != 0 and type_ != 1:
        resp = {'err_msg': 'parameter invalid'}
        return HttpResponse(serializers.serialize('json', resp), "application/json")

    user = User.objects.filter(id=user_id)
    if len(user) != 1:
        resp = {'err_msg': 'user not exist'}
        return HttpResponse(serializers.serialize('json', resp), "application/json")
    movie_list = []
    if type_ == 0:
        movie_list = HaveWatchedList.objects.filter(user=user[0])
    elif type_ == 1:
        movie_list = WouldLikeList.objects.filter(user=user[0])
    sum_movie = len(movie_list)
    paginator = Paginator(movie_list, count)
    try:
        movie_list = paginator.page(offset)
    except PageNotAnInteger:
        movie_list = paginator.page(1)
    except EmptyPage:
        movie_list = paginator.page(paginator.num_pages)
    except InvalidPage:
        # request offset not exist
        resp = {'err_msg': 'request page not exist'}
        return HttpResponse(json.dumps(resp), "application/json")
    movies = []
    for record in movie_list.object_list:
        movies.append(record.want_watch_movie)
    tmp_resp = serializers.serialize("json", movies)
    resp = {'total': sum_movie, 'data': json.loads(tmp_resp)}
    return HttpResponse(json.dumps(resp), "application/json")


def get_rate_list(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if check_token(token) is False:
        resp = {'err_msg': 'token check error'}
        return HttpResponse(json.dumps(resp), "application/json", status=400)
    user_id = get_userid(token)
    user = User.objects.filter(id=user_id)
    if len(user) != 1:
        resp = {'err_msg': 'user not exist'}
        return HttpResponse(json.dumps(resp), "application/json")
    records = UserRate.objects.filter(user=user[0])
    tmp_resp = []
    for record in records:
        movie = record.movie
        tmp_resp.append({'movie_id': movie.movie_id, 'rate': record.rate})
    resp = {'data': tmp_resp}
    return HttpResponse(json.dumps(resp), "application/json")


def get_tag_list(request):
    param = json.loads(request.body)
    movie_id = param.get('movie_id')
    offset = param.get('offset')
    count = param.get('count')
    if movie_id is None or offset is None or count is None:
        resp = {'err_msg': 'parameter invalid'}
        return HttpResponse(json.dumps(resp), "application/json")
    movie_id = int(movie_id)
    offset = int(offset)
    count = int(count)
    movie = Movie.objects.filter(movie_id=movie_id)
    if len(movie) != 1:
        resp = {'err_msg': 'movie id is not exist'}
        return HttpResponse(json.dumps(resp), "application/json")
    tag_list = UserTag.objects.filter(movie=movie[0]).order_by('-votes')
    sum_num = len(tag_list)
    paginator = Paginator(tag_list, count)
    try:
        tag_list = paginator.page(offset)
    except PageNotAnInteger:
        tag_list = paginator.page(1)
    except EmptyPage:
        tag_list = paginator.page(paginator.num_pages)
    except InvalidPage:
        # request offset not exist
        resp = {'err_msg': 'request page not exist'}
        return HttpResponse(json.dumps(resp), "application/json")
    tags = []
    for record in tag_list.object_list:
        tags.append({'user_name': record.user.nick_name, 'content': record.tag, 'time': str(record.tag_time)[:-13],
                     'votes': record.votes, 'tag_id': record.id})
    resp = {'total': sum_num, 'data': tags}
    return HttpResponse(json.dumps(resp), "application/json")


def get_recommend_list(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    param = json.loads(request.body)
    offset = int(param.get('offset'))
    count = int(param.get('count'))
    if check_token(token) is False:
        resp = {'err_msg': 'token check error'}
        return HttpResponse(json.dumps(resp), "application/json", status=400)
    user_id = get_userid(token)
    user = User.objects.filter(id=user_id)
    if len(user) != 1:
        resp = {'err_msg': 'user not exist'}
        return HttpResponse(json.dumps(resp), "application/json")
    user_key = str(user_id) + '_rec'
    movies = cache.get(user_key)
    movie_list = movies.split()
    res_movies = []
    index = 0
    for movie_id in movie_list:
        if index < count * (offset - 1):
            index += 1
            continue
        movie = Movie.objects.filter(id=movie_id)
        res_movies.append(movie[0])
        if len(res_movies) == count:
            break
    tmp_movies = serializers.serialize("json", res_movies)
    resp = {'data': json.loads(tmp_movies), 'total': len(movie_list)}
    return HttpResponse(json.dumps(resp), "application/json")


def vote_tag(request):
    tag_id = request.POST.get('vote_id')
    if tag_id is None:
        resp = {'err_msg': 'invalid param'}
        return HttpResponse(json.dumps(resp), "application/json")
    tag_id = int(tag_id)
    tag = UserTag.objects.filter(id=tag_id)
    if len(tag) != 1:
        resp = {'err_msg': 'tag doesn\'t exsits'}
        return HttpResponse(json.dumps(resp), "application/json")
    tag[0].votes += 1
    try:
        tag[0].save()
    except ValueError as err:
        resp = {'err_msg': err}
        return HttpResponse(json.dumps(resp), "application/json")
    return HttpResponse()

