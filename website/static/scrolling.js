


let textBox = document.getElementById('inputbox');
let label = document.getElementById('label');
const testString = document.getElementById('label').innerHTML;

var presses = 0;
        textBox.addEventListener('keypress', (event) => {
            presses++;
            //style="border:none; background: transparent; outline: 0;"
            //document.getElementById('label').innerHTML =
            alert(testString.slice(presses));
        });