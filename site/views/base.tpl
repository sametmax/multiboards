<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Multiboards - les infos fraîches de vos sites préférés</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
          content="Multiboards regroupe les derniers posts des meilleurs sites du web.">
    <link rel="shortcut icon" href="/static/img/favicon.ico">
    <link href="http://fonts.googleapis.com/css?family=Asap" rel="stylesheet" type="text/css">
    <link href="/static/css/bootstrap.min.css" rel="stylesheet"> 
    <link href="/static/css/bootstrap-responsive.css" rel="stylesheet">
    <link href="/static/css/style.css?2" rel="stylesheet"> 
    <link href="/static/css/jquery.zrssfeed.css?23" rel="stylesheet"> 
    <link href="/static/css/jquery.superbox.css" type="text/css" media="all" rel="stylesheet" />

    <!-- Le HTML5 shim, for IE7-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js" type="text/javascript"></script> 
    <script src="/static/js/bootstrap.min.js"></script> 
    <script src="/static/js/jquery.tipsy.js"></script>
    <script src="/static/js/behavior.js?2"></script>
    <script src="/static/js/jquery.zrssfeed.js?233" ></script>
    <script src="/static/js/jquery.superbox.js?2"></script>
    <script src="http://code.jquery.com/ui/1.9.1/jquery-ui.js"></script>
    <script src="/static/js/player.js"></script>
  </head>

  <body>

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container ">
          <a class="btn btn-navbar" data-toggle="collapse"
             data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <div class="brand hidden-phone">
            <a href="/"><strong>Multi</strong>boards<span>.net</span></a>
          </div>
          <div id="player" class="hidden-phone">
            <span class="btn-play"><i class="icon-white icon-pause hide-it"></i><i class="icon-white icon-play"></i></span>
            <span class="pl-title">Radios...</span>
            <span class="btn-list"><i class="icon-white icon-list"></i></span>
            <ul class="playlist hide-it">
              %for radio, url in settings.RADIOS:
                <li audiourl="{{ url }}">{{ radio }}</li>
              %end
            </ul>
          </div>

          <div class="nav-collapse">
            <ul class="nav">

              %for i, entry in enumerate(settings.MENU):
                <li class="divider-vertical"></li>
                <li>
                  %if "mailto:" in entry[1]:
                    <span title="{{ entry[1].replace('mailto:', '').replace('@', '__AT__') }}"
                          class="email-link" >
	                	%if entry[2]:
	                		{{entry[2]}}
	                	%end
                      {{ entry[0] }}
                    </span>
                  %else:
                    <a href="{{ entry[1] }}">
	                	%if entry[2]:
	                		{{!entry[2]}}
	                	%end
                    	{{ entry[0] }}
                    </a>
                  %end

                </li>
              %end
            </ul>


            <span class="pull-right upper-right"> 
              <div class="nav-collapse">
                <ul class="nav">
                  <li class="divider-vertical"></li>
                  <li><a href="/build">Créer un Board</a></li>
                  <li class="divider-vertical"></li>
                  <li class="dropdown">
                    <a href="#"
                          class="dropdown-toggle"
                          data-toggle="dropdown">
                          <span id="boards-list">Les boards populaires</span>
                          <b class="caret"></b>
                    </a>
                    <ul class="dropdown-menu">
                      <li><a href="#" >Boards name a </a></li>
                      <li><a href="#" >Boards name b </a></li>
                      <li><a href="#" >Boards name c </a></li>
                      <li><a href="#" >Boards name d </a></li>
                      <li><a href="#" >Boards name e </a></li>
                    </ul>
                  </li>
                  <li class="divider-vertical"></li>
                </ul>
              </div>

              <span class="about ">
                "Le meilleur du web"<br>
                <span id="subtitle">sur une seule page...</span>
              </span>
            </span>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
  
    <div class="container well" > 
	           %include
        	<div class="push"></div>
    </div><!--/wrap-content-->
 
      <footer class="container-fluid footer"> 
        <p> 
           <strong>Powered by <a href="http://sametmax.com">Sam&amp;Max</a> - 2012-20..</strong>
           <span id="bottom-line">2 + 2 = 5.</span> 
       </p>
        <span> 
            <div id="online-users">
              <img src="/static/img/people.png">
              <div class="counter"></div>
              personnes connectées
            </div>
       </span>
      </footer> 


  </body>

  <script type="text/javascript">

    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-39400849-1']);
    _gaq.push(['_trackPageview']);

    (function() {
      var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
      ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
      var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();

  </script>
</html>
