$(function() {

    var setupTrello = function() {
        var URL = 'http://172.16.2.101:8000/';
        window.location.href = 'https://trello.com/1/authorize?response_type=token&key=e42346614529e890c100cd4ab4235bac&return_url=' + URL + '&callback_method=getMessage&scope=read,write&expiration=1hour&name=PetRainbow';
    };

    var showList = function() {

        $('button').click(function(e) {
            e.preventDefault();
            console.log($('#name').val());

            $.ajax({
                url: '/name/',
                method: 'POST',
                data: 'name=' + $('#name').val() + '&token=' + localStorage.getItem('token'),
            })
            .success(function(data) {
                for (var i=0; i<data.yesterday.length; i++) {
                    $('.yesterday-list').append('<li>' + data.yesterday[i] + '</li>');
                    // console.log(data.yesterday[i]);
                }

                for (var i=0; i<data.today.length; i++) {
                    $('.today-list').append('<li>' + data.today[i] + '</li>');
                    // console.log(data.yesterday[i]);
                }

            })
            .error(function(e) {
                setupTrello();
            });
        })
        // var query = "https://api.trello.com/1/lists/" + myList + "/cards?key=e42346614529e890c100cd4ab4235bac&token=" + token;
    }
     
    if (typeof(localStorage) !== 'undefined') {
        var URL = window.location.href;
        if (URL.indexOf('#token') > 0) {
            var token = URL.split('#')[1].split('=')[1];
            localStorage.setItem('token', token);
            //here
            showList();
        } else {
            token = localStorage.getItem('token');
            if (!token) {
                setupTrello();
            } else {
                //here
                showList();
            }
        }
     }

});
