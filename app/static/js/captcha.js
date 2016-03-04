function refresh_captcha() {
    var jqxhr = $.ajax("/captcha/captcha_refresh/", {
        contentType : 'application/json',
        type: 'GET',
      }).done(function(data) {
        $("#captcha-image").attr("src", data.image_url);
        $("#captcha-audio").attr("href", "/captcha/captcha_audio/" + data.key);
        $("#captcha-hash").attr("value", data.key);
      }).fail(function() {
        console.log("error refreshing captcha");
      });
}