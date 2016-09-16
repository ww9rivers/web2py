var c9r = c9r || {};
$.extend(c9r, function ()
{
var pv =			// Private variable space
{
	button_css: "ui-state-default ui-corner-all",
	frame1: null,

get_body: function() {
	return pv.get_frame1().contents().find("body");
},

get_frame1: function() {
	return pv.frame1 = pv.frame1 || $("iframe");
},

resize_frame: function() {
	var frame1 = pv.get_frame1();
	var that = pv.get_body();
	if (frame1 && that) {
		var xh = that.height()+8;
		var xfh = frame1.height();
		if (xfh < 8 || (xfh != xh && xfh < 3200 && xh > 8)) {
			c9r.hide_components();	// To be sure!
			var f1footer = that.find("div.splunkified.shared-footer");
			if (f1footer) { f1footer.hide(); }
			console.log("Resize iframe: height="+xh);
			frame1.height(xh);
		}
	}
}
}; // pv - private

var public =
{
hide_components: function() {
	var that = pv.get_body();
	if (!that) {
		console.log("iframe not found.");
		return;
	}
	// console.log("Hiding the Splunk app navigation.");
	that.find(".layoutRow.appHeader").hide();	// Splunk 6
	that.find(".layoutRow.messaging").hide();
	that.find("div.panel-footer>.pull-left>[href!='#export']").hide();
	that.find(".shared-splunkbar").hide();
	that.find(".accountBarItems").hide();		// Splunk 5
	//	Maybe make this configurable?
	// that.find("li.nav-item").hide();
	that.find("a.app-link").removeAttr("href");
},

hide_navigation: function() {
	var frame1 = pv.get_frame1();
	if (!frame1) {
		console.log("iframe not found.");
		return;
	}
	frame1.height(1).show().ready(function() {
		c9r.hide_components();
		setInterval(pv.resize_frame, 1000);
	});
}
}; // public


$(document).ready(function() {
	$("iframe").hide().load(c9r.hide_navigation);
	// console.log('Setup iframe.ready!');
});

return public;
}());
