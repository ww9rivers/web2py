<%@ page language="java" %>
<%@ page pageEncoding="UTF-8" contentType="text/html; charset=UTF-8"%>
<%@ page import="java.util.*" %>
<%@ page import="com.novell.nidp.*" %>
<%@ page import="com.novell.nidp.authentication.local.X509Class" %>
<%@ page import="com.novell.nidp.resource.*" %>
<%@ page import="com.novell.nidp.resource.jsp.*" %>
<%@ page import="com.novell.nidp.ui.*" %>

<%

	response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate"); // HTTP 1.1.
	response.setHeader("Pragma", "no-cache"); // HTTP 1.0.
	response.setDateHeader("Expires", 0); // Proxies.

	Cookie cookie = new Cookie("JSESSIONID", null);
	cookie.setPath(request.getContextPath());
	cookie.setMaxAge(0);
	response.addCookie(cookie);

	response.setHeader("Connection", "close");
	Cookie c = new Cookie(X509Class.X509_LOGOUT_COOKIE, X509Class.X509_LOGOUT_COOKIE_VALUE);
	c.setPath(request.getContextPath());
	response.addCookie(c);
	UIHandler uh = new UIHandler(request,response);
	ArrayList logoutStrings = null;
	ArrayList logos = null;
    if (uh.isJSPMsg())
    {
    	NIDPLogoutMessage msg = 
            (NIDPLogoutMessage)uh.getMessage(true);

        if (msg.isConfirmLogouts())
	    {
        	logoutStrings = ((NIDPLogoutMessage)msg).getStrings();
	       	logos = ((NIDPLogoutMessage)msg).getLogos();
        }
    }

%>
<!DOCTYPE HTML PUBLIC "-//W3C//Dtd HTML 4.0 transitional//<%=uh.getLanguageCode()%>">
<html lang="<%=uh.getLanguageCode()%>">
    <head>
<%
	String app = request.getParameter("app");
	if (app != null) {
		// Redirect after 3 seconds, if an app page is specified:
%>
		<script type="text/javascript">
			setTimeout(function()
			{
				window.top.location.href = "<%=app%>";
			}, 3000);
		</script>
<%
	}
%>
        <link href="<%= uh.getImage("hf_style.css",false)%>" rel="stylesheet">
	    <style type="text/css" media="screen"><!--
		body  { background-color: <%=uh.getBGColor()%> }
	  --></style>
    </head>
    <body marginwidth="0" marginheight="0" leftmargin="10" topmargin="0">
        <div class="head3b"><%=uh.getResource(JSPResDesc.LOGOUT)%></div>		
	    <table border=0>
	        <tr>
	            <td><%=uh.getResource(JSPResDesc.LOGOUT_SUCCESS_MSG)%></td>
 	        </tr>
<%
	if (logos != null && logos.size() > 0)
    {
%>
	    	<tr>
		  	    <td>
                    <table cellSpacing=7 cellPadding=0 align=left border=0>
                        <tr>
                            <td width=15><img height=1 src="<%=uh.getImage("spacer.gif",false)%>" width=15 border=0 alt=""></td>
                            <td colspan="2"><b><%=uh.getResource(JSPResDesc.LOGOUT_SITES)%></b></td>
                        </tr>
		<%
                for (int i = 0; i < logos.size(); i++)
                {
        %>
                        <tr>
                            <td width="15"><img height=1 src="<%=uh.getImage("spacer.gif",false)%>" width=15 border=0 alt=""></td>
                                        <td class=leadCopy><%= (String)logos.get(i) %></td>
                                        <%
                                                String s = (String)logoutStrings.get(i);
                                                if((s != null) && (s.indexOf("?") != -1))
                                                {
                                        %>
                                                <td><iframe id="remoteContent" src="<%= s %>"  WIDTH=0 HEIGHT=0 frameborder=0></iframe> </td>
                                        <%
                                                }
                                                else
                                                {
                                        %>
                                                <td><img alt="<%=uh.getResource(JSPResDesc.LOGOUT)%>" src="<%= s %>"/></td>
                                        <%
                                                }
                                        %>
                                </tr>
        <%
                }
        %>
  
                    </table>
		  		</td>
	    	</tr>
<%    } %>
		</table>
    </body>
</html>
<%request.getSession().invalidate();%>
