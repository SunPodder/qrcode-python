
const imgFile = document.querySelector("input[type='file']"),
  fill = document.querySelector("#fill"),
  bg = document.querySelector("#bg")

document.querySelector("form")
.addEventListener("submit", e => {
  if(imgFile.files.length != 0 && (bg.value != "" | fill.value != "")){
    Toastify({
      text: "Your selected configuration has performance issue.",
      duration: 5000,
      close: true,
      gravity: "bottom", // `top` or `bottom`
      position: "right", // `left`, `center` or `right`
      stopOnFocus: true, // Prevents dismissing of toast on hover
      style: {
        background: "#E52B50",
      }
    }).showToast();
    
    Toastify({
      text: "It may take some time.",
      duration: 6000,
      close: true,
      gravity: "bottom", // `top` or `bottom`
      position: "right", // `left`, `center` or `right`
      stopOnFocus: true, // Prevents dismissing of toast on hover
      style: {
        background: "#E52B50",
      }
    }).showToast();
  }
})