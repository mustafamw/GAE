$(document).ready(function() 
{
	$("input:file").change(function ()
	{
		var form_import = $(this).attr('id');
		var filename = $(this)[0]['files'][0].name;
		console.log(form_import)
		$("#form_import."+form_import).css({'opacity':'1'})
		$("label#"+form_import+" span").text(filename);
	});
	
	$("#login_container form").submit(function()
	{
		var username = $("#username").val();
		var password = $("#password").val();
		
		if(username == '')
		{
			$("#username").css({'border':'1px solid red'})
			return false;
		}
		if(password == '')
		{
			$("#password").css({'border':'1px solid red'})
			return false;
		}
	});
	
});