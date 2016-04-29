function load_share_buttons() {
    if($('#socialshareprivacy').length > 0){
        $('#socialshareprivacy').socialSharePrivacy({
            services : {
                facebook : {
                    'perma_option' : 'off',
                    'dummy_img' : '/static/socialshareprivacy/images/facebook_share_de.png'

                },
                twitter : {
                    'perma_option' : 'off',
                    'dummy_img' : '/static/socialshareprivacy/images/dummy_twitter.png'
                },
                gplus : {
                    'status' : 'off'
                }
            },
            "css_path"  : "/static/socialshareprivacy/socialshareprivacy.css",
            "lang_path" : "/static/socialshareprivacy/lang/",
            "language"  : "de",
            "size" : 'small',
            "uri" : 'https://callfordemocracy.org'
        });
    }
}
