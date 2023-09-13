function toggleMenu(target) {
    let x = document.getElementById(target);
    if (x.classList.contains("display-non")) {
      x.classList.remove("display-non")
    } else {
      x.classList.add("display-non")
    }
}

function hideMenu(target) {
    let x = document.getElementById(target);
    x.classList.add("display-non")
}


function closeModal(){
  let x = document.getElementById("info-modal");
  x.classList.add("display-non");
}

