  localStorage = window.localStorage;

  usuarioinfo = document.getElementById("nombre");

  nombreusuario = document.getElementById("nombreusuario");

  cerrarsesion = document.getElementById("cerrarsesion");

  if (usuarioinfo.value != '') {
    localStorage.setItem("usuarioinfo", usuarioinfo.value)
  }

  if(localStorage.getItem("usuarioinfo")) {
    nombreusuario.innerHTML = localStorage.getItem("usuarioinfo")

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
    window.location = '/home';
  })
 
