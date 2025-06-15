const userId = "{{ request.user.instructorprofile.id }}";
const socket = new WebSocket(`ws://${window.location.host}/ws/notifications/${userId}/`);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    alert("🔔 " + data.message); // Or show in a notification component
};

socket.onclose = function() {
    console.log('WebSocket connection closed');
};


var menuBtn = document.getElementById("menuBtn");
var sideNav = document.getElementById("sideNav");

sideNav.style.right ="-250px";
menuBtn.onclick = function(){
    if(sideNav.style.right == "-250px"){
         sideNav.style.right = "0";
        }
     else{
        sideNav.style.right ="-250px"
        }
    }