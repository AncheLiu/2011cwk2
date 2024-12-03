document.addEventListener('DOMContentLoaded', function() {
    var box = document.getElementById('box');
    var imgbox = document.getElementById('imgbox');
    var img = imgbox.children;
    var back = document.getElementById('back');
    var next = document.getElementById('next');
    var navspan = document.getElementById('nav').children;
    
    var num = 1;
    var onOff = true; // prevent change quickly
    var timer = null;
    var classarr = ['img2', 'img1', 'img3'];
    
    // show when mouse
    box.onmouseover = function() {
        back.style.display = 'block';
        next.style.display = 'block';
        clearInterval(timer);
    }
    
    // hide when no mouse
    box.onmouseout = function() {
        back.style.display = 'none';
        next.style.display = 'none';
        timer = setInterval(nextImg, 3000);
    }
    
    // next
    next.onclick = function() {
        if(onOff) {
            onOff = false;
            nextImg();
            setTimeout(function() {
                onOff = true;
            }, 500);
        }
    }
    
    // last
    back.onclick = function() {
        if(onOff) {
            if(num > 1) {
                num--;
            } else {
                num = 3;
            }
            onOff = false;
            removenav(navspan[num-1]);
            var lastValue = classarr.pop();
            classarr.unshift(lastValue);
            for(var i = 0; i < classarr.length; i++) {
                img[i].className = classarr[i];
            }
            setTimeout(function() {
                onOff = true;
            }, 500);
        }
    }
    
    // change time
    timer = setInterval(nextImg, 2500);
    
    // auto change
    function nextImg() {
        if(num < 3) {
            num++;
        } else {
            num = 1;
        }
        removenav(navspan[num-1]);
        var firstValue = classarr.shift();
        classarr.push(firstValue);
        for(var i = 0; i < classarr.length; i++) {
            img[i].className = classarr[i];
        }
    }
    
    // point change
    function removenav(obj) {
        for(var i = 0; i < navspan.length; i++) {
            navspan[i].className = '';
        }
        obj.className = 'select';
    }
});