import requests
import secrets
from cache import cache
from datetime import timedelta, datetime
# SUCCESS HTTP CODES (200 - 399)
# HTTP_CODES = [200, 201, 202, 203, 204, 205, 206, 207, 301, 302, 303, 304, 305, 306, 307, 308]

# for spical chars ., - and decimal number starting from 0 - 9
URL_STRING_SET = list(range(45, 58))

# for uppercase letters from A - Z
URL_STRING_SET.extend(range(64,91))

# remove / (47 rep.) from the list
URL_STRING_SET.pop(2) 

# string set for our new short url
STRING_SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 

def validateUrl(url: str) -> bool:
    """ check if url is returning success response 
        url - String 
    """
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        req = requests.get(url)
        return req.status_code >= 200 and req.status_code < 400
    
    except:
        return False
    
def generateUrl(custom = None):
    if custom:
        pass
    else:
        return generateString()


def generateString() -> str:
    """ recurcive function untile new string is found"""

    key = "".join(secrets.choice(STRING_SET).lower() for _ in range(5))
    
    db_check = checkDB(key)

    """ call generate again if not unique """
    if db_check:
        return generateString()
    return key


def checkDB(url: str, id: str = None) -> bool:
    """ check if string is unique in the database """
    from models.short_url import ShortUrl
    foundData =  ShortUrl.query.filter_by(short_url = url.lower()).first()
    if foundData:
        if id and foundData.id == id:
            return False
        return True
    return False

def validCustomUrl(custom_url: str):
    """ validate if custom url follow url rules """
    new_url = ""
    for s in custom_url:
        if ord(s.upper()) in URL_STRING_SET:
            new_url = new_url + s
        else:
            new_url = new_url + "-"
    return new_url.lower()


def generate_stat(data: list) -> dict:
    """ Generate the statistics for the last week 
        data - list of ShortUrl
    """
   
    
    current_date = datetime.now().date()

    # Get the start date of the week (Monday)
    start_date = current_date - timedelta(days=6)

    # Initialize the statistics dictionary
    stats = []
    total = len(data)

    # Iterate over each day of the week
    for i in range(7):
        date = start_date + timedelta(days=i)
        formatted_date = date.strftime("%Y-%m-%d")

        # Calculate the number of user registrations for the day
        user_count = sum(
            1 for item in data
            if item.created_at.date() <= date <= item.updated_at.date()
        )
        stats.append({"title": formatted_date, "value": user_count})
        # stats[formatted_date] = user_count


    return {"stats":stats, "total": total}

@cache.memoize()
def daily_limits (user_id:str) -> dict:
    from models.short_url import ShortUrl
    daily_limit_used = ShortUrl.query.filter_by(user_id = user_id).where(ShortUrl.created_at >= (datetime.now().date() - timedelta(days=1))).count()
    daily_limit = 10
    print(daily_limit_used)
    if daily_limit_used >= daily_limit:
        return {"status":True, "message":f"Daily limit of {daily_limit} reached"}
    else:
        return {"status":False, "message":f"From your {daily_limit} daily limit you have {daily_limit - daily_limit_used} left"}