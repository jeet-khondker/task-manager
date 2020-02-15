/* console.log("JavaScript Code Running Successfully!"); 

Sounds: https://www.fesliyanstudios.com/royalty-free-sound-effects-download/crumbling-paper-87 */

function playDelSound(el) {
    var delSound = document.createElement("audio");
    var link = el.srcElement.attributes.href.textContent; 

    delSound.src = "/sounds/delete.mp3";
    delSound.play();
    setTimeout(function(){window.location = link;}, 1000);
    el.preventDefault(); 
}