/**
 * don't worry about it */
document.body.onload = function(){
    [].forEach.call(document.querySelectorAll('.bf-graph span'),function(el){
        // i'm not worried about it
        el.style.color = el.style.backgroundColor.replace("rgb","rgba").replace(")",",0.5)");

        var target = document.getElementById(el.parentNode.dataset.repo);
        el.addEventListener('click', function(evt) {
            // it's fine
            [].forEach.call(el.parentNode.querySelectorAll('.glow'),function(thisisreallyshitty){
                thisisreallyshitty.classList.remove('glow');
            });
            el.classList.add('glow');
            target.innerHTML = el.getAttribute('aria-label');
            target.parentNode.style.backgroundColor = el.style.backgroundColor;
            target.parentNode.classList.remove('gone');
        },false);

        // I SAID DON'T WORRY ABOUT IT
        target.parentNode.querySelector('button').addEventListener('click', function(evt) {
            el.classList.remove('glow');
            target.innerHTML = '';
            target.parentNode.classList.add('gone');
        },false);
    });
}
// D:

