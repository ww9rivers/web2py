$(document).ready(function(){
	var date = new Date();
	var dateString = ('0' + (date.getMonth()+1)).slice(-2)  
		             + ('0' + (date.getDate()-1)).slice(-2)
		             + date.getFullYear().toString().slice(-2);

	//create the url for the daily shift report
	var sdDSR = "http://www.med.umich.edu/i/mcit-tos/24hrDailyReport"
		sdDSR = sdDSR + dateString + ".html"

	$("#daily").attr("href", sdDSR);
});