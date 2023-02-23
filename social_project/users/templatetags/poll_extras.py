from django import template

from users.models import UserMaster

register = template.Library()


@register.filter(name="mutual_friend_count")
def mutual_friend_count(request_user, user_obj):
    data = {"count": 0, "names": ""}
    request_user_friends = request_user.friends.all()
    user_obj_friends = user_obj.friends.all()
    if request_user_friends.count() > 0 and user_obj_friends.count() > 0:
        similar_friends_qs = user_obj_friends.filter(id__in=request_user_friends.values_list('id', flat=True))
        data = {"count": similar_friends_qs.count(), "names": similar_friends_qs.values_list('first_name', flat=True)}
    return data