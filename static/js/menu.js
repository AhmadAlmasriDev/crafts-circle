const userMenu = document.getElementById('user-menu')
const barMenu = document.getElementById('center-nav-menu')
const userMenuButton = document.getElementById('user-menu-button')
const barMenuButton = document.getElementById('bar-menu-button')

document.addEventListener('click', (e) => {
   if (!userMenuButton.contains(e.target)) userMenu.classList.add('display-non')
   if (!barMenuButton.contains(e.target)) barMenu.classList.add('display-non')
 })

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



 