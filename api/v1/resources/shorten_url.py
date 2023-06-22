from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.short_url import ShortUrl, Visitor
from utils.depend import validateUrl, generateUrl, checkDB, validCustomUrl, daily_limits, generate_stat
from cache import cache

shortener = Blueprint("shortener", __name__)


@shortener.route("/")
@jwt_required()
@cache.cached()
def index():
    """ 
        Get all short urls
        ---
        tags:
          - Shortener
        responses:
          200:
            description: Short urls created
          422:
            description: Validation error
          401:
            description: Unauthorized
    """
    args = request.args
    page = args.get("page", 1, type = int)
    per_page = args.get("per_page", 10, type = int)
    
    query_url = ShortUrl.query.filter_by(user_id = get_jwt_identity())  \
            .order_by(ShortUrl.created_at.desc()).paginate(page = page, per_page = per_page)
    
    data = [item.to_json() for item in query_url]
    return jsonify(status = "ok", total = query_url.total, page = query_url.page, per_page = query_url.per_page, data = data)

@shortener.route("/<url>", methods=["GET"])
@jwt_required()
def url(url):
    """ 
        Get a short url
        ---
        tags:
          - Shortener
        parameters:
          - in: path
            name: url
            schema:
              type: string
              description: short url
              example: google
        responses:
          200:
            description: Short url created
          422:
            description: Validation error
          401:
            description: Unauthorized
    """
    
    req_url = ShortUrl.find_by_short_url(url)
    
    stat = generate_stat(req_url.visitors)

    data = { **req_url.to_json()}

    data.pop('visitors')
    
    return jsonify(data = data, **stat), 200

@shortener.route("/<url>/visitors", methods=["GET"])
@jwt_required()
def visitors(url):
    """ 
        Get visitors of a short url
        ---
        tags:
          - Shortener
        parameters:
          - in: path
            name: url
            schema:
              type: string
              description: short url
              example: google
        responses:
          200:
            description: Short url created
          422:
            description: Validation error
          401:
            description: Unauthorized
    """
    req_url = ShortUrl.find_by_short_url(url)

    args = request.args

    page = args.get("page", 1, type = int)
    per_page = args.get("per_page", 10, type = int)
    
    query_visitors = Visitor.query.filter_by(short_url_id = req_url.id).order_by(Visitor.created_at.desc()).paginate(page = page, per_page = per_page)
    visitors = [item.to_json() for item in query_visitors.items]
    return jsonify({"status": "ok", "total": query_visitors.total, "page": query_visitors.page, "per_page": query_visitors.per_page, "data": visitors}), 200


@shortener.route("/generate", methods=["POST"])
@jwt_required()
def create():
    """ 
        Create a new short url
        ---
        tags:
          - Shortener
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                url:
                  type: string
                  description: url to shorten
                  example: https://www.google.com
                custom_url:
                  type: string
                  description: custom url to shorten
                  example: google
        responses:
          201:
            description: Short url created
          422:
            description: Validation error
          401:
            description: Unauthorized
    """
    user_id = get_jwt_identity()

    form_data = request.json
    url = form_data.get("url")
    custom_url = form_data.get("custom_url")
    check_daily_limit = daily_limits(user_id)

    if check_daily_limit['status']:
        return jsonify({
            "status": "error",
            "message": check_daily_limit['message']
        }), 422

    elif url == None:
        return jsonify({
            "status": "error",
            "message": "url field is required"
        }), 422
    
    check_url = validateUrl(url)

    if not check_url:
        return jsonify({
            "status": "error",
            "message": "url not working"
        })
    
    is_custom = custom_url != None

    if is_custom:
        short_url = validCustomUrl(custom_url)
        db_check = checkDB(short_url)
        if db_check:
            return jsonify({
                "status": "error",
                "message": "custom url already taken, try again"
            })
    else:
        short_url = generateUrl()


    new_short_url = ShortUrl(url = url, short_url = short_url, user_id = user_id, is_custom = is_custom)
    new_short_url.save()


    cache.delete_memoized(daily_limits, user_id)

    cache.delete_memoized(ShortUrl.find_by_short_url, ShortUrl, short_url)

    check_limit = daily_limits(user_id)

    cache.delete('view/' + url_for('webShortUrl.history_url_list_page'))

    cache.delete('view/' + url_for('api.shortener.index'))

    return jsonify(status = "ok", data = new_short_url.to_json(), message = "url created", limit = check_limit['message']), 201

@shortener.route("/<url>/edit", methods=["PATCH"])
@jwt_required()
def edit(url):
    """ function to edit url in db
    :param url: url to be edited
    :return: json response
      """
    user_id = get_jwt_identity()
    req = request.json
    data = {}
    query_data = ShortUrl.find_by_short_url(url)

    if user_id != query_data.user_id:
        return jsonify({
            "status": "error",
            "message": "you are not allowed to edit this url"
        }), 403

    if data.get("url"):
        check_url = validateUrl(data.get("url"))

        if not check_url:
            return jsonify({
                "status": "error",
                "message": "url not working"
            })
        data['url'] = req.get("url")
        
    if req.get("custom_url"):
        custom_url = validCustomUrl(req.get("custom_url"))
        
        db_check = checkDB(custom_url, query_data.id)
        if db_check:
            return jsonify({
                "status": "error",
                "message": "custom url already taken, try again"
            })
        
        data['is_custom'] = True
        data["short_url"] = custom_url

    form = query_data.bm_update(data) 

    cache.delete_memoized(ShortUrl.find_by_short_url, ShortUrl, url)

    cache.delete('view/' + url_for('webShortUrl.history_url_list_page'))

    cache.delete('view/' + url_for('api.shortener.index'))

    
    return jsonify(status = "ok", message = "URL updated successfully", data = form), 200

@shortener.route("/<url>/delete", methods=["DELETE"])
@jwt_required()
def delete(url):
    """ function to delete url from db
    :param url: url to be deleted
    :return: json response
      """
    user_id = get_jwt_identity()
    query_data = ShortUrl.find_by_short_url(url)

    if user_id != query_data.user_id:
        return jsonify({
            "status": "error",
            "message": "you are not allowed to delete this url"
        }), 403


    query_data.delete()

    cache.delete_memoized(ShortUrl.find_by_short_url, ShortUrl, url)

    cache.delete('view/' + url_for('webShortUrl.history_url_list_page'))

    cache.delete('view/' + url_for('api.shortener.index'))

    return jsonify(status = "ok", message = 'URL deleted successfully'), 200


