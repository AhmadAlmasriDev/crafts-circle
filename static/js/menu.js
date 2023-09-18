// ______ Hide the menus when click outside ____________________

const userMenu = document.getElementById('user-menu')
const barMenu = document.getElementById('center-nav-menu')
const userMenuButton = document.getElementById('user-menu-button')
const barMenuButton = document.getElementById('bar-menu-button')
const searchBar = document.getElementById('search_bar')

document.addEventListener('click', (e) => {
   if (!userMenuButton.contains(e.target)) userMenu.classList.add('display-non')
   if (!barMenuButton.contains(e.target) & !searchBar.contains(e.target)) barMenu.classList.add('display-non')
 })

// ______ Hide and toggle the menus ____________________________ 
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

// ______ Cloase the modals ____________________________________ 

function closeModal(){
  let x = document.getElementById("info-modal");
  x.classList.add("display-non");
}



 