var canvas = document.querySelector('canvas');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var c = canvas.getContext('2d');

c.font = "250px Arial Black";

function Circle(x, y, z, dx, dy) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.dx = dx;
    this.dy = dy;

    this.draw = function() {
        c.beginPath();
        c.arc(this.x, this.y, this.z, 0, Math.PI * 2, false);
        c.strokeStyle = 'rgba(255,255,255, 0.5)';
        c.stroke();        
    }

    this.update = function() {
        if (this.x > innerWidth || this.x < 0) {
            this.dx = -this.dx;
        }

        if (this.y > innerHeight || this.y < 0) {
            this.dy = -this.dy;
        }
        this.x += this.dx;
        this.y += this.dy;

        this.draw();
    }
}

var circleArray = [];

for (var i = 0; i < 100; i++) {
    var x = Math.random() * window.innerWidth;
    var y = Math.random() * window.innerHeight;
    var z = Math.random() * 50;

    var dx = (Math.random() - 0.5) * 4;
    var dy = (Math.random() - 0.5) * 4;

    circleArray.push(new Circle(x, y, z, dx, dy));

}

var xx = window.innerWidth/3;
var yy =  window.innerHeight/2;

function animate() {

    requestAnimationFrame(animate);
    c.clearRect(0, 0, innerWidth, innerHeight);

    for (var i = 0; i < circleArray.length; i++){
        circleArray[i].update();
    }

    c.strokeText("404", xx, yy);


}

animate();
