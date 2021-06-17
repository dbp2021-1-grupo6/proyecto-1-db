  localStorage = window.localStorage;

  usuairoinfo = document.getElementById("nombre");

  nombreusuario = document.getElementById("nombreusuario");

  cerrarsesion = document.getElementById("cerrarsesion");

  if (usuairoinfo.value != '') {
    localStorage.setItem("usuairoinfo", usuairoinfo.value)
  }

  if(localStorage.getItem("usuairoinfo")) {
    nombreusuario.innerHTML = localStorage.getItem("usuairoinfo")

    navLogOut.removeAttribute('style', 'display:block')
    navLogOut.setAttribute('style', 'display:none')

    navLogIn.removeAttribute('style', 'display:none')
    navLogIn.setAttribute('style', 'display:block')

    console.log("if")
  } else {
    navLogOut.removeAttribute('style', 'display:none')
    navLogOut.setAttribute('style', 'display:block')

    navLogIn.removeAttribute('style', 'display:block')
    navLogIn.setAttribute('style', 'display:none')
    console.log("else")
  }

  cerrarsesion.addEventListener('click', function() {
    localStorage.clear();
    window.location = '/login';
  })
 
