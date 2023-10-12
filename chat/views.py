from django.shortcuts import render, redirect


def index(request):
    nick_name = request.COOKIES.get("nick_name")

    print(nick_name)
    is_nick_name_set = True if nick_name else False

    return render(
        request, "chat/index.html", {"is_nick_name_set": is_nick_name_set}
    )


def room(request, room_name, nick_name):
    if request.method == "POST":
        nick_name = request.POST.get("nick_name")
        return redirect(f"/chat/{room_name}/{nick_name}")

    else:
        response = render(
            request,
            "chat/room.html",
            {"room_name": room_name, "nick_name": nick_name},
        )
        cookies_nick_name = request.COOKIES.get("nick_name")

        if cookies_nick_name and cookies_nick_name == nick_name:
            pass
        else:
            response.set_cookie("nick_name", nick_name)

        return response
