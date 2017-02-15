/**
 * Plugin: jquery.zRSSFeed
 * 
 * Version: 1.1.6
 * (c) Copyright 2010-2012, Zazar Ltd
 * 
 * Description: jQuery plugin for display of RSS feeds via Google Feed API
 *              (Based on original plugin jGFeed by jQuery HowTo. Filesize function by Cary Dunn.)
 * 
 * History:
 * 1.1.6 - Added sort options
 * 1.1.5 - Target option now applies to all feed links
 * 1.1.4 - Added option to hide media and now compressed with Google Closure
 * 1.1.3 - Check for valid published date
 * 1.1.2 - Added user callback function due to issue with ajaxStop after jQuery 1.4.2
 * 1.1.1 - Correction to null xml entries and support for media with jQuery < 1.5
 * 1.1.0 - Added support for media in enclosure tags
 * 1.0.3 - Added feed link target
 * 1.0.2 - Fixed issue with GET parameters (Seb Dangerfield) and SSL option
 * 1.0.1 - Corrected issue with multiple instances
 *
 **/

(function($){

	$.fn.rssfeed = function(url, options, fn) {	
	
		// Set pluign defaults
		var defaults = {
			limit: 10,
			header: true,
			titletag: 'h4',
			date: true,
			content: true,
			snippet: true,
			media: true,
			showerror: true,
			errormsg: '',
			key: null,
			ssl: false,
			linktarget: '_self',
			sort: '',
			sortasc: true,
			title_len: 30
		};  
		var options = $.extend(defaults, options); 
		
		// Functions
		return this.each(function(i, e) {
			var $e = $(e);
			var s = '';

			// Check for SSL protocol
			if (options.ssl) s = 's';
			
			// Add feed class to user div
			if (!$e.hasClass('rssFeed')) $e.addClass('rssFeed');
			
			// Check for valid url
			if(url == null) return false;
			
			// Create Google Feed API address
			//var api = "http"+ s +"://ajax.googleapis.com/ajax/services/feed/load?v=1.0&callback=?&q=" + encodeURIComponent(url);
			var limit = 100;
			if (options.limit != null) limit = options.limit;
			var api = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20xml%20where%20url%20%3D%20\'" + encodeURIComponent(url) + "\'" + "%20limit%20" + limit + "&format=json";
			//if (options.limit != null) api += "&num=" + options.limit;
			//if (options.key != null) api += "&key=" + options.key;
			//api += "&output=json_xml";

			// Send request
			$.getJSON(api, function(data){
				
				var durl = url;
				try{
					
					if (data.query.results.feed){
						//On Success do something.
						// Process the feeds
						var res = data.query.results.feed;
						_process(e, res, options, plan='a');
					}else{
						//On Success do something.
						// Process the feeds
						var res = data.query.results.rss.channel;
						_process(e, res, options, plan='b');
					}

					// Optional user callback function
					if ($.isFunction(fn)) fn.call(this,$e);

				}catch(err){

					if (options.errormsg != '') {
						var msg = options.errormsg;
					} else {
						var msg = data.responseDetails;
					};
					$(e).html('<div class="rssError"><p>problem with '+ url +'</p></div>');

				}

				// Optional user callback function
				//if ($.isFunction(fn)) fn.call(this,$e);

			// }).fail(function(jqXHR) {

			// 	if (options.showerror){
			// 		if (options.errormsg != '') {
			// 			var msg = options.errormsg;
			// 		} else {
			// 			var msg = data.responseDetails;
			// 		};
			// 		$(e).html('<div class="rssError"><p>'+ msg +'</p></div>');
			// 	};

			});


				// // Check for error
				// if (data.responseStatus == 200) {
	
				// 	// Process the feeds
				// 	_process(e, data.responseData, options);

					
				// } else {

				// 	// Handle error if required
				// 	if (options.showerror)
				// 		if (options.errormsg != '') {
				// 			var msg = options.errormsg;
				// 		} else {
				// 			var msg = data.responseDetails;
				// 		};
				// 		$(e).html('<div class="rssError"><p>'+ msg +'</p></div>');
				// };
			//});				
		});
	};
	
	// Function to create HTML result
	var _process = function(e, data, options, plan) {

		// Get JSON feed data
		var feeds = data;
		if (!feeds) {
			return false;
		}
		var rowArray = [];
		var html = '';
		var row = 'odd';
		var row_color = options.odd;
		
		// Get XML data for media (parseXML not used as requires 1.5+)
		if (options.media) {
			var xml = getXMLDocument(data.xmlString);
			var xmlEntries = xml.getElementsByTagName('item');
		}
		
		// Add header if required
		if (plan == 'a') {
			link = options.url;
			description = feeds.title.content;
			title = feeds.title.content;
			entries = feeds.entry;
		}else{
			link = options.url;
			description = feeds.description;
			title = feeds.title;
			entries = feeds.item;
		}
		console.log(plan + ' ' + link);
			
		if (options.header)
			html +=	'<div class="rssHeader thumbnail" style="background-color:#'+options.header_bgcolor+';color:#'+options.header_color+'">' +
				'<a href="'+link+'" title="'+ description +'">'+ title +'</a>' +
				'</div>';
			
		// Add body
		html += '<div class="rssBody ">' +
			'<ul>';

		// Sort feed if required


		// Add feeds
		for (var i=0; i<options.limit; i++) {
			
			rowArray[i] = [];

			// Get individual feed
			var entry = entries[i];
			var pubDate;
			var sort = '';
			var boards_nfo = '';
			var end = '';
			if (plan == 'a') {
				var title = entry.title.content;
				var entry_link = entry.link[0].href;
			}else{
				var entry_link = entry.link;
				var title = entry.title;				
			}


			// Apply sort column
			switch (options.sort) {
				case 'title':
					sort = entry.title;
					break;
				case 'date':
					sort = entry.publishedDate;
					break;
			}
			rowArray[i]['sort'] = sort;

			// Format published date
			if (entry.publishedDate) {
				var entryDate = new Date(entry.publishedDate);
				var pubDate = entryDate.toLocaleDateString() + ' ' + entryDate.toLocaleTimeString();
			}
			
			// Add feed row
			var title_orig = title;
			if(title.length > options.title_length) title = title.substring(0,options.title_length)+'...';

			if (options.end){
				end = '</span><span class="feed-right"><a href="'+entry_link+'?&goto=newpost">fin</a></span>';
			}

			if (options.ucfirst){
				title = ucfirst(title, true);
			}
			rowArray[i]['html'] = '<span class="feed-left"><'+ options.titletag +'> - <a href="'+ entry_link +'" original-title="'+ title_orig.replace(/\"/g,' ') +'">'+ title +'</a></'+ options.titletag +'>'+end;

			if (options.date && pubDate) rowArray[i]['html'] += '<div>'+ pubDate +'</div>'
			if (options.content && plan == 'b') {
			
				// Use feed snippet if available and optioned
				if (options.snippet && entry.contentSnippet != '') {
					var content = entry.contentSnippet.split('>Votez !')[0] ;
				} else {
					var content = entry.content.split('>Votez !')[0] ;
				}
				
				rowArray[i]['html'] += '<p>'+ content +'</p>'
			}
			
			// Add any media
			if (options.media && xmlEntries.length > 0) {
				var xmlMedia = xmlEntries[i].getElementsByTagName('enclosure');
				if (xmlMedia.length > 0) {
					
					rowArray[i]['html'] += '<div class="rssMedia"><div>Media files</div><ul>'
					
					for (var m=0; m<xmlMedia.length; m++) {
						var xmlUrl = xmlMedia[m].getAttribute("url");
						var xmlType = xmlMedia[m].getAttribute("type");
						var xmlSize = xmlMedia[m].getAttribute("length");
						rowArray[i]['html'] += '<li><a href="'+ xmlUrl +'" title="Download this media">'+ xmlUrl.split('/').pop() +'</a> ('+ xmlType +', '+ formatFilesize(xmlSize) +')</li>';
					}
					rowArray[i]['html'] += '</ul></div>'
				}
			}
					
		}
		
		// Sort if required
		if (options.sort) {
			rowArray.sort(function(a,b) {

				// Apply sort direction
				if (options.sortasc) {
					var c = a['sort'];
					var d = b['sort'];
				} else {
					var c = b['sort'];
					var d = a['sort'];
				}

				if (options.sort == 'date') {
					return new Date(c) - new Date(d);
				} else {
					c = c.toLowerCase();
					d = d.toLowerCase();
					return (c < d) ? -1 : (c > d) ? 1 : 0;
				}
			});
		}

		// Add rows to output
		$.each(rowArray, function(e) {

			html += '<li class="rssRow" style="background-color:#'+row_color+'">' + rowArray[e]['html'] + '</li>';

			// Alternate row classes
			if (row == 'odd') {
				row = 'even';
				row_color = options.even;
			} else {
				row = 'odd';
				row_color = options.odd;
			}			
		});

		html += '</ul>' +
			'</div>'
			
		boards_nfo ='';
		if (options.boards_nfo){
			boards_nfo = '<div class="boards-nfo"></div>';
		}

		$(e).html(html+boards_nfo);

		// Apply target to links
		$('a',e).attr('target',options.linktarget);
	};
	
	function ucfirst(str,force){
          str=force ? str.toLowerCase() : str;
          return str.replace(/(\b)([a-zA-Z])/,
                   function(firstLetter){
                      return   firstLetter.toUpperCase();
                   });
    }

	function formatFilesize(bytes) {
		var s = ['bytes', 'kb', 'MB', 'GB', 'TB', 'PB'];
		var e = Math.floor(Math.log(bytes)/Math.log(1024));
		return (bytes/Math.pow(1024, Math.floor(e))).toFixed(2)+" "+s[e];
	}

	function getXMLDocument(string) {
		var browser = navigator.appName;
		var xml;
		if (browser == 'Microsoft Internet Explorer') {
			xml = new ActiveXObject('Microsoft.XMLDOM');
			xml.async = 'false'
			xml.loadXML(string);
		} else {
			xml = (new DOMParser()).parseFromString(string, 'text/xml');
		}
		return xml;
	}

})(jQuery);
