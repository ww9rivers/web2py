$(document).ready(function(){
	$("#tabs").tabs({
		beforeLoad: function( event, ui ) {
            ui.jqXHR.success(function() { 	
            	//two datatables cannot coexist so before you load the tab remove the old table
            	$("#table").remove();
            });
            ui.jqXHR.error(function() {
                ui.panel.html(
                    "Couldn't load this tab. We'll try to fix this as soon as possible. ");
            });
            ui.ajaxSettings.cache = true;
        },
		load: function(event, ui) {
			//load anchor tags in the active tab
			$(ui.panel).delegate('a', 'click', function(event) {
//	            $(ui.panel).load(this.href);
				loadAnchorTable(this,event,ui);
//	            event.preventDefault();
	        });
			
			//initialize the data table widget
			sortTable();
		},
		cookie: {
			expires: 30 
		}
	});
	
	//action to load and resort anchor elements called within a panel
	function loadAnchorTable(a, event, ui){
    	//two datatables cannot coexist so before you load the tab remove the old table
    	$("#table").remove();
    	
		$(ui.panel).load(a.href,null, function(){
	        //initialize the data table widget
			sortTable();
		});
        event.preventDefault();
	}
	
	//this will allow the tab headers to be re-clickable
	$("#tabs ul.ui-widget-header")
	 	.delegate("li.ui-tabs-active","mousedown",function(){
	 		$("#tabs").tabs("load",$(this).index());
	 });  	
});