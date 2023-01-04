document.onwheel = function (event){
	console.log(event)
	if (event.deltaY > 0){
		document.getElementById("roll").innerHTML = "вниз";
	}
	else{
		document.getElementById("roll").innerHTML = "вврех";
	}
}
us1=document.getElementById("user1").innerHTML;
us2=document.getElementById("user2").innerHTML;
const url = '/chat/' + us1 + '/' +us2;

function send_data(){
  data = {
    text: document.getElementById("message_box").value,
    user1: us1,
    user2: us2
  }
  const xhr = new XMLHttpRequest();
  xhr.open('POST', url);
  xhr.responseType = 'json';
  xhr.setRequestHeader('Content-Type','application/json');
  xhr.onload = () => {
  }
  xhr.send(JSON.stringify(data));
};

dan=[];
window.onload = setInterval(function() {
      fetch('/api')
        .then((response) => {
            return response.json();
        })
        .then((myjson) => {
            console.log(myjson);
            if (dan.length == myjson.length){
              console.log(myjson);
              console.log(dan);
            }
            else{
                for (let i=dan.length; i < myjson.length; i++){
                  let liFirst = document.createElement('li');
                  liFirst.className = "mes_li";
                  liFirst.innerHTML = myjson[i];
                  ol.append(liFirst);       
              }
            }
            dan = myjson;
        });
},1000);









