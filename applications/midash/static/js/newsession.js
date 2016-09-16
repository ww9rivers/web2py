/* $Id$
 *
 *	Deleting all session cookies using the jQuery Cookie plugin.
 */

$.cookie().each(function(name, value) {
	if (value.expires == undefined) {
		$.removeCookie(name);
	}
});