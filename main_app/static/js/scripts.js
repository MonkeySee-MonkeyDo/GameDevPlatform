var slideIndex = 0;
var interval = setInterval(() => { changeSlide(1) }, 2000);

function changeSlide(n) {
  var x = document.getElementsByClassName("mySlides");
  for (var i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  slideIndex += n;
  if (slideIndex > x.length-1) { slideIndex = 0 }
  if (slideIndex < 0) { slideIndex = x.length-1 }
  x[slideIndex].style.display = "block";
  clearInterval(interval);
  interval = setInterval(() => { changeSlide(1) }, 2000);
}

document.getElementById("leftArrow").addEventListener("click", ev => { changeSlide(-1) });
document.getElementById("rightArrow").addEventListener("click", ev => { changeSlide(1) });