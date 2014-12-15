/*
 * by Dylan Woodbury
 */

function FoodPic(x, y, xPos, yPos, width, height, img, name, time, comment, score) {
    this.x = x;
    this.y = y;
    this.xPos = xPos;
    this.yPos = yPos;
    this.width = width;
    this.height = height;
    this.img = img;
    this.name = name;
    this.time = time;
    this.comment = comment;
    this.score = score;
    
    this.rating = false;
    this.stage = "static";
    this.cursor = false;
    this.SPEED = 4;
    this.MIN_WIDTH = this.width;
    this.MAX_WIDTH = 360;
    
    this.checkMouse = function(mousePos) {
        
        if(mousePos.x > this.x && mousePos.x < this.x+this.width &&
           mousePos.y > this.y && mousePos.y < this.y+this.height)
            this.cursor = true;
        else
            this.cursor = false;
        
    };
    
    this.checkMouseClick = function(mousePos) {
        if(mousePos.x > this.x && mousePos.x < this.x+this.width &&
           mousePos.y > this.y && mousePos.y < this.y+this.height) {
            if(!this.rating)
                this.rating = true;
            else
                this.rating = false;
        }
        else this.rating = false;
        
    };
    
    this.update = function(active) {
        
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
            this.height += this.SPEED;
            
            if(this.xPos == "center")
                this.x -= this.SPEED/2;
            else if(this.xPos == "right")
                this.x -= this.SPEED;
            
            if(this.yPos == "down")
                this.y -= this.SPEED;
            
            if(this.width >= this.MAX_WIDTH)
                this.stage = "static";
        }
        
        if(this.stage != "decrease" && this.width > this.MIN_WIDTH && active=="arrow")
            this.stage = "decrease";
            
        if(this.stage == "decrease") {
            this.width -= this.SPEED;
            this.height -= this.SPEED;
            
            if(this.xPos == "center")
                this.x += this.SPEED/2;
            else if(this.xPos == "right")
                this.x += this.SPEED;
            
            if(this.yPos == "down")
                this.y += this.SPEED;
            
            if(this.width == this.MIN_WIDTH)
                this.stage = "static";
        }
        
    };
    
    this.getLength = function(words) {
        var length = 0;
        var numWords = words.length;
        length += numWords-1;
        for(var i=0; i < numWords; i++) {
            length += words[i].length;
        }
        return length;
    };
    
    this.draw = function(context) {
        
            context.drawImage(this.img, this.x, this.y, this.width, this.height);
        if(this.rating) {
            context.fillStyle = "rgba(255,255,0,.7)";
            context.beginPath();
            context.rect(this.x, this.y, this.width, this.height);
            context.fill();
            context.fillStyle = "#000000";
            context.font = "20px Arial";
            context.fillText(this.name, this.x+15, this.y+25);
            context.fillText(this.time, this.x+15, this.y+45);
            
            var words = this.comment.split(" ");
            var lineNum = 0;
            var lines = [];
            lines[0] = this.comment;
            /*for(var i=0; i < words.length; i++) {
                var word = words[i];
                if(this.getLength(lines[lineNum])+word.length+1 < 30) {
                    lines[lineNum].push(word);
                } else {
                    lineNum++;
                    lines[lineNum].push(word);
                }
            }*/
            context.fillText("Comments: " + lines[0], this.x+15, this.y+85);
            context.fillText("Score: " + this.score + "/5", this.x+15, this.y+115);
            /*for(var i=1; i < this.lines.length; i++)
                context.fillText(this.lines[i], this.x+25, this.y+105+(i*20));*/
            
        }
    };
    
}
