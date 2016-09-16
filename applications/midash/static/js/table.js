function sortTable(){
	var table = $("#table").dataTable({
		"bAutoWidth": false,
	    "sScrollY": "50em",
	    "bScrollCollapse": true,
		"bDeferRender": true,	
		"bJQueryUI": true,
	    "bPaginate": false,
	    "bProcessing": true,
	    "bDestroy": true,
	    "bStateSave": true,
	    "fnDrawCallback": function( oSettings ) {
	    	//TODO do something on callback?
	    },
	    "oLanguage": {
	        "sSearch": "Filter: "
	    }
	});	
	return table;
}
