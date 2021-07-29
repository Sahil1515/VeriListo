
static files
```
    import os   
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
```

include image 

        body{
            background-image: url("{% static 'body_bg_image.png' %}");
            background-color: #cccccc;
        }

image settings
        https://www.webfx.com/blog/web-design/responsive-background-image/



         $('#add_btn').click(function () {
                var input_ele = $("#input").val()
                if (input_ele != "") {

                    append_ele = "<li class='cross' class='unchecked'>" + input_ele + "</li>"
                    $("ul").append(append_ele)
                }
            })





https://www.youtube.com/watch?v=NG48CLLsb1A



 django-admin startproject mysite

 python manage.py startapp polls