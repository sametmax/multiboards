$(function(){


/* Parse obfuscaded emails and make them usable */
$('.email-link').each(function(i, elem){
  var $obfuscatedEmail = $(this);
  var address = $obfuscatedEmail.attr('title').replace('__AT__', '@');
  var text = $obfuscatedEmail.text().replace('__AT__', '@');
  var $plainTextEmail = $('<a href="mailto:' + address + '">'+ text +'</a>');
  $obfuscatedEmail.replaceWith($plainTextEmail);

});

var boards_colors = {};

var options = {
    date: false,
    content: false,
    snippet: false,
    media: false,
    showerror: false,
    span: 3,
    linktarget: '_blank',
    header_color: 'FFF',
    setted_colors: false
};

function shuffle(o){ //v1.0
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
}

function loadDatas()
{
  /* Main boards list generator */
  $.getJSON("/json/sources?short_url=" + $('#row-boards').attr('data-short-url'), function(data) {
    $('#row-boards').html('');
    $.each(data, function(i,item){
      options.title_length = 40;
      options.limit= 10;
      options.header_bgcolor = item[3];
      options.odd = item[4];
      options.even = item[5];
      options.content = false;
      options.boards_nfo = true;
      options.end =  false;
      options.ucfirst = true;
      if(item[2].length){
        $('<div class="span'+options.span+' thumbnail" id="board-'+i+'"></div>').appendTo('#row-boards');
        $('#board-'+i+'').rssfeed(item[2], options, function(){
          /*  title helper  */
          $("#row-boards a").hover(
            function () {
              $(this).parents('.rssFeed').children('.boards-nfo').html($(this).attr('original-title'));
            },
            function () {
              $(this).parents('.rssFeed').children('.boards-nfo').html('');
            }
          );
        });
      }
    });
  });

  /* Bottom news list generator */
  $.getJSON("/json/news", function(data) {
    $('#row-bottom-news').html('');
    $.each(data, function(i,item){
      options.title_length = 100;
      options.limit= 5;
      options.header_bgcolor = 'BBB';
      options.header_color = '212121';
      options.odd = 'FFF';
      options.even = 'FFF';
      options.content = false;
      options.boards_nfo = false;
      options.end =  false;
      $('<div class="span3" id="'+slugify(item[0])+'"></div>').appendTo('#row-bottom-news');
      $('#'+slugify(item[0])+'').rssfeed(item[1], options);
    });
  });

  /* DTC news & VDM */
  $('#dtc-bottom-news').html('');
  $('#vdm-bottom-news').html('');
  options.title_length = 100;
  options.limit= 1;
  options.header_color = '212121';
  options.header_bgcolor = 'BBB';
  options.odd = 'FFF';
  options.even = 'FFF';
  options.content = true;
  options.boards_nfo = false;
  options.end =  false;
  $('<div class="span3" id="dtc"></div>').appendTo('#dtc-bottom-news');
  $('#dtc').rssfeed("http://danstonchat.com/items.xml", options);
  $('<div class="span3" id="vdm"></div>').appendTo('#vdm-bottom-news');
  $('#vdm').rssfeed("http://feeds.feedburner.com/viedemerde", options);


  /* Scan some imgur funs */
  $.getJSON("/json/imgur", function(data) {
    var imgs = '';
    $('#imgur-thumbs').html('');
    $.each(data, function(i, items){
      for (var i = 0; i < 17; i++) {
        try {
          var tr = items[i]['hash'];
        imgs=imgs+'<span><a href="http://i.imgur.com/'+items[i]['hash']+items[i]['ext']+'" rel="superbox[gallery][my_gallery]" original-title="'+items[i]['title']+'"><img src="http://i.imgur.com/'+items[i]['hash']+items[i]['ext']+'" width="60" height="60" original-title="'+items[i]['title']+'"></a></span>';
        }
        catch(err)
        {}
      }
    });
    $(imgs).appendTo('#imgur-thumbs');
  })
  .success(function() {
    /* superbox */
    $.superbox();

    /*  tooltips for sharing button */
    $('#imgur-thumbs a').tipsy({fade: true, gravity: 'n'});

  });

  /* change bottom line */
  changeBottomLine();

  /* Get online users */
  $.getJSON("/online", function(data) {
      $("#online-users .counter").html(data['online_users']);
  });

  /* refresh every 10 mins */
  setTimeout(loadDatas, 60*10*1000);
}

/* Load datas then refresh every 10 mins */
if($('#row-boards').length){

  /* load imgur, boards, bottom lines */
  loadDatas();

  /* Load Radio */
  var $player = $('#player');

  if ($player.length) {


    /* Populate radio dropdown */
    $.getJSON("/json/radios", function(data) {
      $.each(data, function(i,item){
        if(item.title.length > 50) item.title = item.title.substring(0,47)+'...';
        $('<li><a href="'+item.url+'">'+item.title+'</a></li>').appendTo("#radios");
      });
    });


    /* Click a radio link */
    $('.dropdown-menu li a').bind("click", function(e){
      e.preventDefault();
      var $this = $(this);

      try {var this_id = $this.attr('id');}
      catch(err){var this_id = '';}

      if ( this_id == 'volume-down' ){
        var volume = jwplayer().getVolume();
        if (volume < 10){volume = 10;}
        jwplayer().setVolume(volume-10);
      } else if (this_id == 'volume-up'){
        var volume = jwplayer().getVolume();
        if (volume > 90){volume = 90;}
        jwplayer().setVolume(volume+10);
      } else if (this_id == 'volume-off'){
        jwplayer().stop();
      } else {

        /* Load audio player */
        jwplayer("player").setup({
            flashplayer: "/static/player/player.swf",
            height: '24px',
            file: $(this).attr('href'),
            width: '324px',
            allowfullscreen: 'false',
            controlbar: 'bottom',
            type: 'sound',
            autostart: true
        });

        /* if radio was stopped restart it*/
        var volume = jwplayer().getVolume();
        if (!volume){jwplayer().setVolume(10);}

        /* set title */
        $('#radio-title').html($this.html());


      }


    });

  }

}

/* Build custom boards */
if($('#build').length){

  function url_domain(data) {
    var a = document.createElement('a');
    a.href = data;
    return a.hostname;
  }


  function set_colors(domain, id, url) {
    /* get colors */

    $.post('/favicon', {url: domain}, function(url){
        $('<img>').append('body').hide().attr('src', url);
    });

    $.ajax({
      url: "/build/colors/" + domain,
      context: document.body
    }).done(function(data) {
      boards_colors[domain] = data;
      if(data != 'error'){

        bc = eval(boards_colors[domain]);

        /* Add some sweet colors for odd & even */
        bc.push('eee');
        bc.push('fff');

        /* Define board colors */
        options.header_bgcolor = bc[0];
        options.odd = bc[1];
        options.even = bc[2];
        options.setted_colors = true;

        /* add colors picker to board */
        // var colors_list = '';
        // $(bc).each(function(index, value){
        //   colors_list += '<li style="background-color:' + value + ';"></li>';
        // });
        // $(".colors-" + id).html('<div class="board-options"><ul>' + colors_list +  '</ul></div>');

        refresh_board(id, url);
      }
    });
  }

  function refresh_board(id, url) {

    var domain = url_domain(url);
    var current = $("#" + id);

    if(!options.setted_colors){
      options.header_bgcolor = "aaa";
      options.odd = "fff";
      options.even = "eee";
    }

    // Custom options
    options.title_length = 40;
    options.limit= 10;
    options.content = false;
    options.boards_nfo = true;
    options.end =  false;
    options.ucfirst = true;

    /* build board */
    current.html('<p class="bold center">Loading data...</p>');
    current.attr('data-url', url);
    current.attr('data-name', domain);

    current.rssfeed(url, options, function(e){
      if(options.setted_colors === false){
        set_colors(domain, id, url);
      }else{
        options.setted_colors = false;
      }

    });

  }

  /* make list sortable */
  $( "#sortable" ).sortable();
  $( "#sortable" ).disableSelection();

  /* submit flux */
  function submit_flux(e) {

    var url = $('#board-url').val();
    var filled = false;
    var code = e.keyCode || e.which;
    // on Enter
    if(code == 13 || e.type == 'paste' || e.type == 'click'){
      // check empty slot, then add new feed
      $("#sortable").find($(".board-container")).each(function(){
        var current = $(this);
        if( ( current.find($(".board-wrapper")).attr('data-url') === undefined && filled === false )|| current.find($(".board-wrapper")).attr('data-url') == url ) {
          /* build board */
          refresh_board(current.find(".board-wrapper").attr('id'), url);
          /* set slot as taken */
          filled = true;
        }
      });
    }

  }

  function save_board(){

    /* get array */
    var boards = [];
    $(".board-container").each(function(){
        boards.push(  $(this).index() + ";" +
                      $(this).find($(".board-wrapper")).attr('data-url') + ";" +
                      'aaa' + ";" +
                      'fff' + ";" +
                      'eee'
                   );
    });

    /* Save current position */
    $.post( "/build/save", { 'urls': JSON.stringify(boards), "uuid": $("#board-url").attr('data-uuid') } )
      .done(function( data ) {
        $("#custom-url").html(data);
        $("#custom-url").show();
    });
  }


  $( "#board-url" ).bind("keypress", function(e) {
    submit_flux(e);
    save_board();
  });

  $( "#submit-flux" ).bind("click", function(e) {
    submit_flux(e);
    save_board();
  });

  /* Save board config */
  $("#sortable").on("sortupdate", function( event, ui ) {
    save_board();
  });


} /* end build */


function slugify(Text)
{
    return Text
        .toLowerCase()
        .replace(/ /g,'-')
        .replace(/[^\w-]+/g,'')
        ;
}

function changeBottomLine(){
  $.get("/json/bottomline", function(data) {
    $("#bottom-line").html(data);
  });
}


$('.popup').click(function(event) {
    var width  = 630,
        height = 450,
        left   = ($(window).width()  - width)  / 2,
        top    = ($(window).height() - height) / 2,
        url    = this.href,
        opts   = 'status=1' +
                 ',width='  + width  +
                 ',height=' + height +
                 ',top='    + top    +
                 ',left='   + left;

    window.open(url, 'Share media', opts);

    return false;
});


}); /* End of "document ready" jquery callback */