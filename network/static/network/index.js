document.addEventListener('DOMContentLoaded', function(){
  console.log("In Index.js.");

  //Defalut displaying all posts
  document.querySelector("#all-posts").style.display = "block";
  document.querySelector("#create-post").style.display = "none";


});


function createPost(){
  document.querySelector("#all-posts").style.display = "none";
  document.querySelector("#create-post").style.display = "block";

  var error = document.querySelector("#message");
  console.log("Near Button");

  //Adding event Listener
  document.getElementById("create-button").addEventListener('click',(event) => {
    event.preventDefault();
    title = document.querySelector("#title");
    post = document.querySelector('#post');
    fetch(`/create`,{
      method: "POST",
      body: JSON.stringify({
        title: title.value,
        post: post.value,
      }),
    })
    .then(response => response.json())
    .then(result => {
      if(result.status == 200){
        error.innerHTML = `<div class="alert alert-success" role="alert">${result.message}</div>`;
      }else {
        error.innerHTML = `<div class="alert alert-danger" role="alert">${result.error}</div>`;
      }
    })
  })
}
