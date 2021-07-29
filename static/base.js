
    $(document).ready(function () {
        var url = window.location;

        $('ul.nav li a').filter(function() {
            return this.href == url;
        }).addClass('active');
    });