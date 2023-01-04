function del_text() {
  document.getElementById("message_box").value = "";
  document.getElementById("message_box").style.color = "black";
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
  del_text();
};

dan=[];
window.onload = setInterval(function() {
      us = ({'user1':us1,'user2':us2})
      fetch('/api/'+us1+'/'+us2)
        .then((response) => {
            return response.json(us);
        })
        .then((myjson) => {
            console.log(myjson);
            if (dan.length == myjson.length){
              console.log(myjson);
              console.log(dan);
            }
            else{
                for (let i=dan.length; i < myjson.length;i++){
                  let liFirst = document.createElement('li');
                  if (myjson[i] == us1){
                    liFirst.className = "mes_li_my";
                  }else{
                    liFirst.className = "mes_li_he";
                  }
                  mes = myjson[i]+ ": " +myjson[i+1];
                  liFirst.innerHTML = mes;
                  ol.append(liFirst);
                  i++;       
              }
            }
            dan = myjson;
        });
},1000);









