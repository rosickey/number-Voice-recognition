//  flashSound 1.2 - jQuery 1.4.2 plugin by bootleq@gmail.com 2010-05-30
//  http://www.bootleq.com/item/flashSound/
/*
    USAGE:

    style 1:

        $.flashSound( 'foo.mp3', {id: 'se1'} );
        $.flashSound.play('se1');
        $.flashSound.play('se1', true);   // stop previous before play
        $.flashSound.stop('se1');
        $.flashSound.remove('se1');

    style 2:

        var se1 = $.flashSound( 'foo.mp3' );
        se1.play();
        se1.play(true);    // stop previous before play
        se1.stop();
        se1.remove();

    shared between 2 styles:

        $.flashSound({ id: 'foo', swf: 'path/flashSound.swf' });
        $.flashSound.enable();
        $.flashSound.disable();
        $.flashSound.setEnabled(true);  // same as toggle(true)
        $.flashSound.isEnabled();
        $.flashSound.toggle();

*/

(function($) {

var tracks  = {};
var enabled = true;

var nextId = function(){  // 新增 object 時，要用的 id
    var r = 0;
    while( $('#sound_'+r).length ) { r++; }
    return 'sound_'+r;
};

var template = function(aId, aSwf, aUrl) {
    return '<object sap-type="object" sap="object" id="'+ aId +'" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/" height="0" width="0">'
    + '<param name="movie" value="'+ aSwf +'" /><param name="FlashVars" value="url='+ aUrl +'" /><param name="allowScriptAccess" value="always" /><param name="loop" value="false" /><param name="quality" value="low" />'
    + '<embed name="'+ aId +'" src="'+ aSwf +'" FlashVars="url='+ aUrl +'" type="application/x-shockwave-flash" allowScriptAccess="always" quality="low" loop="false" pluginspage="http://www.adobe.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" height="0" width="0" /></object>';
};

var play = function(aMono) {
    if( aMono && typeof(this.swf_stop)=='function' ) { this.swf_stop(); }
    if( enabled && typeof(this.swf_play)=='function' ) { this.swf_play(); }
};

var stop = function() {
    if( typeof(this.swf_stop)=='function' ) { this.swf_stop(); }
};

var remove = function(aId) {
    $('#'+aId).remove();
    tracks[aId] = null;
};

$.extend({
    flashSound: function( aUrl ) {
        var options = $.extend( {}, $.flashSound.defaults, arguments[1] );
        if(aUrl.constructor != String) { return; }

        var id = options.id ? options.id : nextId();

        if(tracks[id]) { remove.call(null, tracks[id].obj); }   // 移除 id 相同的物件（以免重複）

        var obj = document.createElement('div');    // 新增一個 div 來放 flash 影片
        document.body.appendChild( obj );
        obj.innerHTML = template( id, options.swf, aUrl );

        if (navigator.appName.indexOf("Microsoft") != -1) { obj = obj.firstChild; }
        else { obj = $(obj).find('embed').get(0); }

        tracks[id] = {
            obj: obj,
            play: function(aMono){ play.call(obj, aMono); },
            stop: function(){ stop.call(obj); },
            remove: function(){ remove.call(null, id); }
        };

        return tracks[id];
    }
});

$.flashSound.play = function(aId, aMono) {
    if(tracks[aId]) return play.call(tracks[aId].obj, aMono);
};

$.flashSound.stop = function(aId) {
    if(tracks[aId]) return stop.call(tracks[aId].obj);
};

$.flashSound.remove = function(aId) {
    if(tracks[aId]) return remove.call(null, aId);
};

$.flashSound.enable = function() {
    enabled = true;
};

$.flashSound.disable = function() {
    enabled = false;
    for( i in tracks) {
        if(tracks[i] && tracks[i].stop) tracks[i].stop();
    }
};

$.flashSound.setEnabled = function(aEnabled) {
    if(aEnabled) {
        $.flashSound.enable();
    } else {
        $.flashSound.disable();
    }
};

$.flashSound.isEnabled = function() {
    return enabled;
};

$.flashSound.toggle = function(aEnabled) {
    if (typeof aEnabled == 'boolean') {
        $.flashSound.setEnabled(aEnabled);
    } else {
        $.flashSound.setEnabled(!enabled);
    }
};

//$.flashSound.onSwfReady = function(aId) { };

$.flashSound.defaults = {
    id : null,
    swf: 'flashSound.swf'
};

})(jQuery);
