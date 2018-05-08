//<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.js"></script>
    // var script = document.createElement('script');
     
    // script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.js';
    // document.getElementsByTagName('head')[0].appendChild(script); 
	
	$(document).ajaxStart(function() {
		$("#modal").show();
		$("#fade").show();
		}).ajaxStop(function() {
		$("#modal").hide();
		$("#fade").hide();
	});

	$(document).ready(function () {
		$("button").click(function () {
			loadFun();
			//console.log("alert");
			$.ajax({
				url: "http://localhost:3000/MyGitContributionsAPI?uname="+$('#rand').val(),
				type: "GET",
				//data: { uname: $('#rand').val() },
				success: function (response) {
					if (response.status == 404) {
						alert("sdgdf");
						$("#index_output").html("No such user found.");
					}
					else {
						//alert("ok response");
						console.log("data  ",JSON.parse(JSON.stringify(response)));
						var contributionsObject = JSON.parse(JSON.stringify(response));
						myFunction1(contributionsObject)

					}
				},
				error: function (response) {
				$("#index_output").show();
				$("#index").hide();
				$("#myTable").hide();
				$("#index_output").html("No such user found."+response);
				}
			});
		});
	});

	//myFunction();
	
	function loadFun(){
		$("#loading").hide();
		document.getElementById('index_output').style.display= "none";
		document.getElementById('index').style.display = 'none';
	}
	var date_diff_indays = function(date1, date2) {
		dt1 = new Date(date1);
		dt2 = new Date(date2);
		return Math.abs(Math.floor((Date.UTC(dt2.getFullYear(), dt2.getMonth(), dt2.getDate()) - Date.UTC(dt1.getFullYear(), dt1.getMonth(), dt1.getDate()) ) /(1000 * 60 * 60 * 24)));
	}
	function myFunction1(contributionsObject) {
		let output_arr = new Array(365).fill(0);        // initialize array of 365 with all 0s
		let output_arr_rel_data = new Array(365).fill(0);
		let current_date = new Date();
		let last_year = new Date(new Date().getTime()-365*1000*60*60*24);
		last_year.setHours(0,0,0,0);
		console.log(last_year);
		let index;
		var input = document.getElementById( 'input_date' ).value;
		var select_date = new Date(input);
		var new_search = [];
		for(var i=0; i<contributionsObject.length; i++){
			parts = contributionsObject[i].date.split("/");
			console.log(parts);
			temp_date = new Date(20+parts[2], parts[0] - 1, parts[1]);
			temp_date.setHours(0,0,0,0);
			console.log(temp_date);
			index = date_diff_indays(last_year,temp_date)//((temp_date-last_year)/(1000*60*60*24))
			console.log(temp_date);
			console.log(last_year);
			if(!!select_date.valueOf() && temp_date>select_date){
				console.log(index+" pushed here");
				new_search.push(index);
			}
			output_arr[index] = contributionsObject[i].commits + contributionsObject[i].pull_requests + contributionsObject[i].issues + contributionsObject[i].create_repo;
			output_arr_rel_data[index] = "Date: "+ contributionsObject[i].date+"; Commits:"+ contributionsObject[i].commits+"; pull_Req:" + contributionsObject[i].pull_requests +"; Issues:" +contributionsObject[i].issues + "; Repos_created:"+contributionsObject[i].create_repo
		}
	
	

		if ( !!select_date.valueOf() ) { // Valid date, then display dates in date range
			console.log("valid");
			var table = document.getElementById("myTable");
			var row, cell1, cell2;
			var rowCount = table.rows.length;
			document.getElementById('index_output').style.display = 'block';
			document.getElementById('myTable').style.display = 'table';
			document.getElementById('index').style.display = 'block';
			for (var i = rowCount - 1; i > 0; i--) {
				table.deleteRow(i);
			}
			let total_contr = 0;
			console.log("I write  is written here");
			for (var i = 0; i < new_search.length; i++) {
				if(output_arr[new_search[i]]!=0){
					row = table.insertRow(1);
					cell1 = row.insertCell(0);
					cell2 = row.insertCell(1);
					total_contr += output_arr[new_search[i]];
					cell1.innerHTML = output_arr[new_search[i]]+" Contributions on "+output_arr_rel_data[new_search[i]].split(';').slice(0,1);
					cell2.innerHTML = output_arr_rel_data[new_search[i]].split(';').slice(1);
				}
			}
			document.getElementById('index_output').innerHTML = "<p><strong> Contribution of user: " + $('#rand').val()+
				" after date - "+select_date.toString().split(' ').slice(0, 4).join(' ')+" is  <u>"+total_contr+"</u><p>Please note - all contributions visible on date "
					+last_year.toString().split(' ').slice(0, 4).join(' ')+
					" are cumulative contributions on and before of "+last_year.toString().split(' ').slice(0, 4).join(' ')+"</p></strong></p>";
		}
		else{
			document.getElementById('index_output').style.display = 'block';
			document.getElementById('index_output').innerHTML = "<h2><strong> Contribution Array of user: " + $('#rand').val() + "</strong></h1><br>"+
				"<p>Please note - all contributions visible on date "+last_year.toString().split(' ').slice(0, 4).join(' ')+" are cumulative contributions on and before of "+last_year.toString().split(' ').slice(0, 4).join(' ')+"</p>";
			//document.getElementById('repositories_output').innerHTML = "<span>"+output_arr[354]+"</div>"//"<span class='tooltip'>"+output_arr[354] +" ,<span class='tooltiptext'>jamba</span></span>";
			document.getElementById('repositories_output').innerHTML = "{";
			for(var i=0; i<output_arr.length; i++){
				document.getElementById('repositories_output').innerHTML += "<span class='tooltip_1'>"+output_arr[i] +" ,<span class='tooltiptext_1'>"+output_arr_rel_data[i]+"</span></span>";
				//$('repositories_output').add("<span class='tooltip'>"+output_arr[i] ,+"<span class='tooltiptext'>"+output_arr_rel_data[i]+"</span></span>")
			}
			document.getElementById('repositories_output').innerHTML += "}";
		}
	}    
