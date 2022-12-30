function del_text() {
	document.getElementById('message_box').innerHTML = "";
	document.getElementById('message_box').style.color = "black";
}

document.onwheel = function (event){
	console.log(event)
	if (event.deltaY > 0){
		document.getElementById("roll").innerHTML = "вниз";
	}
	else{
		document.getElementById("roll").innerHTML = "вврех";
	}
}