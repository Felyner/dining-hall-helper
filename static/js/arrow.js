function arrow(x,y,width,height) {
    this.x = x;
        this.MIN_X = this.x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.MIN_WIDTH = this.width;
    this.MAX_WIDTH = this.width+18;
    this.SPEED = 2;
    this.stage = "static";
    this.cursor = false;
    
    this.checkMouse = function(mousePos) {
        
        if((mousePos.x > this.MIN_X-25 && mousePos.x < this.MIN_X+this.width && this.x < 200) ||
              (mousePos.x < this.MIN_X+55 && mousePos.x > this.MIN_X && this.x > 200))
            this.cursor = true;
        else
            this.cursor = false;
        
    };
    
    this.update = function() {
        
        if(this.cursor) {
            if(this.width < this.MAX_WIDTH)
                this.stage = "increase";
            else
                this.stage = "static";
        }
        else {
            if(this.width > this.MIN_WIDTH)
                this.stage = "decrease";
            else
                this.stage = "static";
        }
        
        if(this.stage == "increase") {
            this.width += this.SPEED;
            if(this.x < 200)
                this.x -= this.SPEED;
            
            if(this.width >= this.MAX_WIDTH)
                this.stage = "static";
        }
        else if(this.stage == "decrease") {
            this.width -= this.SPEED;
            if(this.x < 200)
                this.x += this.SPEED;
            
            if(this.width <= this.MIN_WIDTH)
                this.stage = "static";
        }
        
    };
    
    this.draw = function(ctx) {
        ctx.fillStyle = "rgba(0,0,255,.3)";
        ctx.fillRect(this.x,this.y,this.width,this.height);
        ctx.strokeStyle = "rgba(255,255,255,1)";
        ctx.lineWidth=2;
        if(this.x < 200) {
            ctx.beginPath();
            ctx.moveTo(this.MIN_X+20, this.height/2);
            ctx.lineTo(this.MIN_X+this.MIN_WIDTH-20, this.height/2+10);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(this.MIN_X+20, this.height/2);
            ctx.lineTo(this.MIN_X+this.MIN_WIDTH-20, this.height/2-10);
            ctx.stroke();
        }
        else {
            ctx.beginPath();
            ctx.moveTo(this.MIN_X+this.MIN_WIDTH-20, this.height/2);
            ctx.lineTo(this.MIN_X+20, this.height/2+10);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(this.MIN_X+this.MIN_WIDTH-20, this.height/2);
            ctx.lineTo(this.MIN_X+20, this.height/2-10);
            ctx.stroke();
        }
        
    };
}
