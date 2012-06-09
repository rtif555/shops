<script type="text/javascript">
$(document).ready(function(){
						   
	$(window).resize(function(){

		$('.center').css({
			position:'absolute',
			left: ($(window).width() - $('.center').outerWidth())/2			
		});
		
	});
	// To initially run the function:
	$(window).resize();

});
	  
</script>