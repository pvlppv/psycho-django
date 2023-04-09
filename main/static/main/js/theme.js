const toggle = document.querySelector('#hero-settings-theme');
const root = document.documentElement;
const blackColor = getComputedStyle(root).getPropertyValue("--black-color");
const whiteColor = getComputedStyle(root).getPropertyValue("--white-color");
const blackshadowColor = getComputedStyle(root).getPropertyValue("--shadow-black-color");
const whiteshadowColor = getComputedStyle(root).getPropertyValue("--shadow-white-color");

let isDarkTheme = localStorage.getItem('darkTheme') !== 'false';

function setTheme(isDarkTheme) {
  if (isDarkTheme) {
    root.style.setProperty("--black-color", blackColor);
    root.style.setProperty("--white-color", whiteColor);
    root.style.setProperty("--shadow-black-color", blackshadowColor);
    root.style.setProperty("--shadow-white-color", whiteshadowColor);
  } else {
    root.style.setProperty("--black-color", whiteColor);
    root.style.setProperty("--white-color", blackColor);
    root.style.setProperty("--shadow-black-color", whiteshadowColor);
    root.style.setProperty("--shadow-white-color", blackshadowColor);
  }
  document.body.removeAttribute('hidden');
}  

setTheme(isDarkTheme);

toggle.addEventListener('click', function(){
  isDarkTheme = !isDarkTheme;
  setTheme(isDarkTheme);
  localStorage.setItem('darkTheme', isDarkTheme);
});