from flask import Blueprint, redirect, render_template, request
from models.short_url import ShortUrl, Visitor
from flask_login import login_required, current_user
from web.forms import NewUrl, UpdateUrl
from utils.depend import validCustomUrl, generateUrl, generate_stat, daily_limits
from cache import cache
import json
from flask import url_for
from flask import flash

webShortUrl = Blueprint("webShortUrl", __name__)


def page_not_found(e):
  return render_template('404.html'), 404

webShortUrl.register_error_handler(404, page_not_found)



@webShortUrl.route("/", methods=["GET", "POST"])
@webShortUrl.route("/custom", methods=["GET", "POST"])
@login_required
def index():
    """ 
    This function is used to redirect the user to the home page.
    It also checks if the user has reached the daily limit.
    """

    user_id = current_user.id

    form = NewUrl(user_id=user_id)

    check_limit = daily_limits(user_id)
  

    if request.method == "POST" and form.validate_on_submit() and not check_limit['status']:
        url = form.url.data
        custom_url = form.custom_url.data


        is_custom = custom_url != None
        
        if is_custom:
            short_url =  validCustomUrl(custom_url)
        else:
            short_url = generateUrl()
        
        form.url.data = None
        form.custom_url.data = None

        short_url = ShortUrl(url = url, short_url = short_url, user_id = user_id, is_custom = is_custom)
        short_url.save()

        cache.delete_memoized(daily_limits, user_id)
        check_limit = daily_limits(user_id)

        cache.delete('view/' + url_for('webShortUrl.history_url_list_page'))

        cache.delete('view/' + url_for('api.shortener.index'))
    

    links_list = ShortUrl.query.filter_by(user_id = current_user.id).order_by(ShortUrl.created_at.desc()).limit(3).all()
    data = [item.to_json() for item in links_list]

    return render_template("index.html", form = form, data = data, daily_limits = check_limit)

@webShortUrl.route("/history")
@login_required
@cache.cached()
def history_url_list_page():
    """ 
    This route is used to show the history page.
    """

    short_url_list = ShortUrl.query.filter_by(user_id = current_user.id).order_by(ShortUrl.created_at.desc()).all()
    all_data = [item.to_json() for item in short_url_list]
    return render_template("history.html", all_data = all_data)

@webShortUrl.route("/history/<url>")
@login_required
def short_url_page(url):
    """ 
    This route is used to show stat based on visitors data of specific url 
    """
    short_url_list = ShortUrl.query.filter_by(user_id = current_user.id).order_by(ShortUrl.created_at.desc()).all()
    all_data = [item.to_json() for item in short_url_list]

    
    query_data = ShortUrl.find_by_short_url(url)
    visitors = Visitor.query.filter_by(short_url_id = query_data.id).order_by(Visitor.created_at.desc()).all()
    stats = generate_stat(visitors)
    
    data = {**query_data.to_json()}
  
    return render_template("history.html", url = url, all_data = all_data, data = data ,  stats = json.dumps(stats))


@webShortUrl.route("/history/<url>/visitors")
@login_required
def short_url_visitors_page(url):
    """ 
    This route is used to show visitors data for specific url
    """
    args = request.args

    page = int(args.get("page", 1))
    per_page = int(args.get("per_page", 10))


    short_url_list = ShortUrl.query.filter_by(user_id = current_user.id).order_by(ShortUrl.created_at.desc())
    all_data = [item.to_json() for item in short_url_list]
    query_data = ShortUrl.find_by_short_url(url)

    query_vistiors = Visitor.query.filter_by(short_url_id = query_data.id).order_by(Visitor.created_at.desc()).paginate(page = page, per_page = per_page)
    data = { **query_data.to_json(), "visitors": query_vistiors}
  
    return render_template("history.html", url = url, all_data = all_data, data = data)


@webShortUrl.route("/history/<url>/edit", methods=["GET", "POST"])
@login_required
def short_url_edit_page(url):
    """ 
    This route is used to edit the short url.
    """

   
    query_data = ShortUrl.find_by_short_url(url)
    form = UpdateUrl(id=query_data.id, short_url = query_data.short_url, url = query_data.url)


    short_url_list = ShortUrl.query.filter_by(user_id = current_user.id).order_by(ShortUrl.created_at.desc())
    all_data = [item.to_json() for item in short_url_list]

    data = { **query_data.to_json()}

    if request.method == "POST" and form.validate_on_submit():
        url = form.url.data
        short_url = form.short_url.data
        
        update_data = query_data.bm_update({"url": url, "short_url": short_url})

        cache.delete('view/' + url_for('webShortUrl.history_url_list_page'))

        cache.delete('view/' + url_for('api.shortener.index'))
    
        return redirect(url_for('webShortUrl.short_url_page', url = short_url))
  
    return render_template("history.html", url = url, all_data = all_data, data = data, form = form)


@webShortUrl.route("/history/<url>/delete")
@login_required
def short_url_delete(url):
    """ 
    This route is used to delete the short url.
    """
    
    user_id = current_user.id

    query_data = ShortUrl.find_by_short_url(url)
    query_data.delete()

    cache.delete_memoized(daily_limits, user_id)

    cache.delete_memoized(ShortUrl.find_by_short_url, ShortUrl, url)

    cache.delete('view/' + url_for('webShortUrl.history_url_list_page'))

    cache.delete('view/' + url_for('api.shortener.index'))

    return redirect(url_for('webShortUrl.history_url_list_page'))

@webShortUrl.route("/<url>")
def redirect_url(url):
    """ 
    This route is used to redirect the user to the original url.
    and update clicks by one 
    """
    
    red_url = ShortUrl.find_by_short_url(url)

    red_url.bm_update({"clicks": red_url.clicks + 1})
   

    Visitor(ip_address = request.remote_addr,
    agent_version = request.user_agent.version,
    agent_platform = request.user_agent.platform,
    short_url_id = red_url.id).save()
    
    cache.delete('view/' + url_for('webShortUrl.short_url_page', url = url))
    cache.delete_memoized(ShortUrl.find_by_short_url, ShortUrl, url)
    
    return redirect(red_url.url)



