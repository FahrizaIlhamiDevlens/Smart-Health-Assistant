const text = "Cek Kesehatan Tubuh Anda Hanya Dengan Satu Klik";
const typing = document.getElementById("typing");

let index = 0;
let hapus = false;

function typeWriter() {

    if (!hapus) {
        typing.textContent = text.substring(0, index + 1);
        index++;

        if (index === text.length) {
            hapus = true;
            setTimeout(typeWriter, 1500);
            return;
        }

    } else {
        typing.textContent = text.substring(0, index - 1);
        index--;

        if (index === 0) {
            hapus = false;
        }
    }

    setTimeout(typeWriter, hapus ? 50 : 100);
}

typeWriter();