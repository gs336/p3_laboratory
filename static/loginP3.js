//登入按鈕

var btn11 = document.getElementById("btn11");
btn11.addEventListener("click",function(){
    //alert("11");
})

var btn11 = document.getElementById("btn11");
btn11.addEventListener("mouseover",function(){
    //alert("11");
    this.style.background = "#8ad9e9";
})

var btn11 = document.getElementById("btn11");
btn11.addEventListener("mouseout",function(){
    //alert("11");
    this.style.background = "#B9EDF8";
})

//註冊按鈕
var trgt = document.getElementById("trgt");
var btn22 = document.getElementById("btn22");
btn22.addEventListener("click",function(){
    //alert("22");
    //trgt.action = "register.html";   //flask不能這樣跳
})

var btn22 = document.getElementById("btn22");
btn22.addEventListener("mouseover",function(){
    //alert("11");
    this.style.background = "rgba(80, 230, 180, 0.794)";
})

var btn22 = document.getElementById("btn22");
btn22.addEventListener("mouseout",function(){
    //alert("11");
    this.style.background = "rgba(138, 255, 216, 0.794)";
})