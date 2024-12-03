$(function() {
    $(".reaction-btn").click(function() {
        var $btn = $(this);
        var movieId = $btn.data('movie-id');
        var reactionType = $btn.data('type');
        var $oppositeBtn = reactionType === 'like' ? $('.dislike') : $('.like');

        $.ajax({
            url: '/movie/' + movieId + '/react',
            type: 'POST',
            data: JSON.stringify({ 
                reaction: reactionType
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                // count like and dislike
                $('.like .reaction-count').text(response.like_count);
                $('.dislike .reaction-count').text(response.dislike_count);
                
                // button active state
                $btn.toggleClass('active');
                $oppositeBtn.removeClass('active');
            },
            error: function(error) {
                console.log('Error:', error);
                alert('please login');
            }
        });
    });
});