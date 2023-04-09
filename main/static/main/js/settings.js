const aboutBtn = document.querySelector('#hero-settings-about');
const aboutWindow = document.querySelector('#hero-settings-about-window');
const langBtn = document.querySelector('#hero-settings-lang');
const langWindow = document.querySelector('#hero-settings-lang-window');
const userBtn = document.querySelector('#hero-settings-user');
const userWindow = document.querySelector('#hero-settings-user-window');
const themeBtn = document.querySelector('#hero-settings-theme');

aboutBtn.addEventListener('click', () => {
  toggleWindow(aboutWindow, 'about');
});

langBtn.addEventListener('click', () => {
  toggleWindow(langWindow, 'lang');
});

userBtn.addEventListener('click', () => {
  toggleWindow(userWindow, 'user');
});

function toggleWindow(window, key) {
  if (window.style.display === 'flex') {
    window.style.display = 'none';
    localStorage.removeItem('window');
  } else {
    aboutWindow.style.display = 'none';
    langWindow.style.display = 'none';
    userWindow.style.display = 'none';
    window.style.display = 'flex';
    localStorage.setItem('window', key);
  }
}

document.addEventListener('click', (event) => {
  if (!aboutBtn.contains(event.target) && !aboutWindow.contains(event.target) && !langBtn.contains(event.target) && !langWindow.contains(event.target) && !userBtn.contains(event.target) && !userWindow.contains(event.target) && !themeBtn.contains(event.target)) {
    aboutWindow.style.display = 'none';
    langWindow.style.display = 'none';
    userWindow.style.display = 'none';
    localStorage.removeItem('window');
  }
});

switch(localStorage.getItem('window')) {
  case 'about':
    aboutWindow.style.display = 'flex';
    break;
  case 'lang':
    langWindow.style.display = 'flex';
    break;
  case 'user':
    userWindow.style.display = 'flex';
    break;
  default:
    break;
}
