/**
 *
 * HTML5 Audio player with playlist
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * Copyright 2012, Script Tutorials
 * http://www.script-tutorials.com/
 */
jQuery(document).ready(function() {

    // inner variables
    var song;
    var title;


    function initAudio(elem) {
        var url = elem.attr('audiourl');
        title = elem.text();
        song = new Audio(url);

    }
    function playAudio() {
        song.play();

        $('.pl-title').html(title);

        $('.icon-play').addClass('hide-it');
        $('.icon-pause').addClass('show-it');
    }
    function stopAudio() {
        song.pause();

        $('.icon-play').removeClass('hide-it');
        $('.icon-pause').removeClass('show-it');
    }

    // play click
    $('.icon-play').click(function (e) {
        e.preventDefault();
        playAudio();
    });

    // pause click
    $('.icon-pause').click(function (e) {
        e.preventDefault();
        stopAudio();
    });

    // show playlist
    $('.icon-list, .pl-title').click(function (e) {
        e.preventDefault();
        
        var pl = $('.playlist');
        if(pl.is(":visible")){
            pl.fadeOut(100);
        }else{
            pl.fadeIn(300);   
        }
    });

    // playlist elements - click
    $('.playlist li').click(function () {
        stopAudio();
        initAudio($(this));
        playAudio();
        $('.playlist').hide();
    });

    // initialization - first element in playlist
    initAudio($('.playlist li:first-child'));

    // set volume
    song.volume = 0.8;

});