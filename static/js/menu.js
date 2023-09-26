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

// ______ Toggle menu __________________________________________

function toggleMenu(target) {
    let x = document.getElementById(target);
    if (x.classList.contains("display-non")) {
      x.classList.remove("display-non")
    } else {
      x.classList.add("display-non")
    }
}

// ______ Modal close __________________________________________

function closeModal(){
  let x = document.getElementById("info-modal");
  x.classList.add("display-non");
}

// ______ Disable buttons after click ______________________________________

const check = ()=>{

  for (item of textInput){
    if (!item.checkValidity()) {
      return false
    }
  }
  for (item of passInput){
    if (!item.checkValidity()) {
      return false
    }
  }
  for (item of textArea){
    if (!item.checkValidity()) {
      return false
    }
  }
  for (item of selectInput){
    if (!item.checkValidity()) {
      return false
    }
  }

  return true
}

const disableButton = () => {
  formButton.disabled = true
}

const action = ()=>{
  if (check()){
    setTimeout(disableButton, 1);  
  }
}

if (document.querySelector('.button')) {
  formButton = document.querySelector('.button');
  textInput = document.querySelectorAll('main input[type="text"]');
  passInput = document.querySelectorAll('main input[type="password"]');
  textArea = document.querySelectorAll('textarea');
  selectInput = document.querySelectorAll('main select');

  formButton.addEventListener('click', action);

}



  


  

 