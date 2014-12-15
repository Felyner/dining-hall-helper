function mainPost() {
	// Basic variables
	canvas = document.getElementById('canvas1');
	this.context = canvas.getContext('2d');
	this.context.fillStyle = 'white';
	this.context.font = "10px Arial";
	this.width = canvas.width;
	this.height = canvas.height;
	this.x;
	this.y;
	
    this.startingPause = 100;
    this.SCROLL_SPEED = 1;
    this.speed = this.SCROLL_SPEED;
    
	this.mode;
    
    this.active = null;
    
    this.loadedToX1;
    this.loadedToX2;
    
    this.topLeftIndices = [];
    this.bottomLeftIndices = [];
    this.topRightIndices = [];
    this.bottomRightIndices = [];
	
    this.names = [];
    this.scores = [];
    this.comments = [];
    this.times = [];
    
    arrows = [];
        arrows.push(new arrow(30,10,50,620));
        arrows.push(new arrow(this.width-80,10,50,620));
    
    this.imgs = [];
    foodPics = [];
    
    this.postObjs = document.postObjs;
    for(var i=0; i<this.postObjs.length; i++) {
        this.imgs[i] = this.postObjs[i].image;
        this.names[i] = this.postObjs[i].user;
        this.scores[i] = this.postObjs[i].rating;
        this.times[i] = this.postObjs[i].time;
        this.comments[i] = this.postObjs[i].comment;
    }
    
  	/*** INIT ***/
  	
  	this.init = function() {
  		
  		this.mode = "pictures";
        var count=0;
        for(var i=-1; i<4; i++) {
            for(var j=0; j<2; j++) {
                var xPos="center";
                
                var yPos="down";
                if(j==0)
                    yPos="up";
                
                    //284
                foodPics.push(new FoodPic(i*this.width/3, j*this.width/3, xPos, yPos, canvas.width/3, canvas.height/2, this.imgs[count], this.names[count], this.times[count], this.comments[count], this.scores[count]));
                count++;
                if(count >= this.postObjs.length)
                    count = 0;
            }
        }/*
        foodPics.push(new FoodPic(this.width/3*-1, 0, "center", "up", canvas.width/3, canvas.height/2, this.imgs[4], this.names[4], this.times[4], this.comments[4], this.scores[4]));
        foodPics.push(new FoodPic(this.width/3*-1, this.width/3, "center", "down", canvas.width/3, canvas.height/2, this.imgs[5], this.names[5], this.times[5], this.comments[5], this.scores[5]));
        foodPics.push(new FoodPic(this.width/3*3, 0, "center", "up", canvas.width/3, canvas.height/2, this.imgs[0], this.names[0], this.times[0], this.comments[0], this.scores[0]));
        foodPics.push(new FoodPic(this.width/3*3, this.width/3, "center", "down", canvas.width/3, canvas.height/2, this.imgs[1], this.names[1], this.times[1], this.comments[1], this.scores[1]));*/
        
       
        this.loadedToX1 = foodPics[6].x*-1;
        this.loadedToX2 = foodPics[8].x+foodPics[8].width-this.width;
        
        for(var i=this.postObjs.length-1; i>=0; i--) {
            if(i%2==0) {
                this.topRightIndices.push(i);
                this.bottomLeftIndices.push(i);
            }
            else {
                this.bottomRightIndices.push(i);
                this.topLeftIndices.push(i);
            }/*
            this.topRightIndices = [0,4,2];
            this.bottomRightIndices = [1,5,3];
            this.topLeftIndices = [5,1,3];
            this.bottomLeftIndices = [4,0,2];*/
        }
        
         function getMousePos(canvas, evt) {
            var rect = canvas.getBoundingClientRect();
            return {
              x: evt.clientX - rect.left,
              y: evt.clientY - rect.top
            };
         }
        
        function sizeArrows(mousePos, arrows, foodPicks) {
            var num=0;
            var cursorFlag=false;
            for(var i=0; i<arrows.length; i++) {
                var arrow = arrows[i];
                arrow.checkMouse(mousePos);
                if(arrow.cursor) {
                    nullFoodPics(foodPics);
                    cursorFlag = true;
                    num++;
                }
            }
            if(!cursorFlag)
                for(var i=0; i<arrows.length; i++)
                    arrows[i].cursor = false;
        }
        
        function moveFoodPics(mousePos, foodPics) {
            for(var i=0; i<foodPics.length; i++) {
                var pic = foodPics[i];
                pic.checkMouse(mousePos);
                if(pic.cursor && this.active == "arrow") {
                    pic.cursor = false;
                }
            }
        }
        
        function nullFoodPics(foodPics) {
            for(var i=0; i<foodPics.length; i++) {
                var pic = foodPics[i];
                pic.cursor = false;
            }
        }
        
        function checkClick(mousePos, foodPics) {
            for(var i=0; i<foodPics.length; i++) {
                var pic = foodPics[i];
                if(this.active != "arrow")
                    pic.checkMouseClick(mousePos);
            }
        }
        
        canvas.addEventListener('mousemove', function(evt){sizeArrows(getMousePos(canvas, evt), arrows, foodPics)}, false);
        canvas.addEventListener('mousemove', function(evt){moveFoodPics(getMousePos(canvas, evt), foodPics)}, false);
        canvas.addEventListener('mouseout', function(evt){nullFoodPics(foodPics)}, false);
        canvas.addEventListener('mousedown', function(evt){checkClick(getMousePos(canvas, evt), foodPics)}, false);
    };
    
  	
  	/*** UPDATE ***/
  	
  	
	this.update = function() {
        
        var lastActive = this.active;
        this.active = null;
        for(var i=0; i<arrows.length; i++) {
            if(arrows[i].cursor)
                this.active = "arrow";
        }
        if(this.active != "arrow" && lastActive == "arrow")
            for(var i=0; i<arrows.length; i++)
                arrows[i].cursor = false;
            
        var change = 0;
        for(var i=0; i<foodPics.length; i++) {
            
            foodPics[i].update(this.active);
            if(this.startingPause <= 0) {
                if(this.active == "arrow") {
                    if(arrows[0].cursor) {
                        change = this.speed*10;
                    }
                    else {
                        change = this.speed*-10;
                        
                    }
                }
                else change = this.speed*-1;
                
                foodPics[i].x += change;
            }
            else if(this.active == "arrow")
                this.startingPause = 0;
        }
        
        this.loadedToX1 -= change;
        this.loadedToX2 += change;
        
        if(this.loadedToX1 < 100) {
            var index1 = this.topLeftIndices.pop();
            var index2 = this.bottomLeftIndices.pop();
            this.topLeftIndices.splice(0,0,[index1]);
            this.bottomLeftIndices.splice(0,0,[index2]);
            foodPics.push(new FoodPic((this.loadedToX1*-1)-this.width/3, 0, "center", "up", canvas.width/3, canvas.height/2, this.imgs[index1], this.names[index1], this.times[index1], this.comments[index1], this.scores[index1]));
            foodPics.push(new FoodPic((this.loadedToX1*-1)-this.width/3, this.width/3, "center", "down", canvas.width/3, canvas.height/2, this.imgs[index2], this.names[index2], this.times[index2], this.comments[index2], this.scores[index2]));
            this.loadedToX1 += canvas.width/3;
        }
        if(this.loadedToX2 < 100) {
            var index1 = this.topRightIndices.pop();
            var index2 = this.bottomRightIndices.pop();
            this.topRightIndices.splice(0,0,[index1]);
            this.bottomRightIndices.splice(0,0,[index2]);
            foodPics.push(new FoodPic(this.width+this.loadedToX2, 0, "center", "up", canvas.width/3, canvas.height/2, this.imgs[index1], this.names[index1], this.times[index1], this.comments[index1], this.scores[index1]));
            foodPics.push(new FoodPic(this.width+this.loadedToX2, this.width/3, "center", "down", canvas.width/3, canvas.height/2, this.imgs[index2], this.names[index2], this.times[index2], this.comments[index2], this.scores[index2]));
            this.loadedToX2 += canvas.width/3;
        }
        
        for(var i=0; i<arrows.length; i++) {
            arrows[i].update();
        }
        
        
        this.startingPause--;
	};
	
	/*** DRAW ***/
	
	
	this.draw = function() {
		
		this.context.clearRect(0,0,this.width,this.height);
		/*this.context.beginPath();
		this.context.rect(0, 0, this.width, this.height);
		this.context.fillStyle = "#113780";
		this.context.fill();*/
		
        var cursorPic = null;
        for(var i=0; i < foodPics.length; i++) {
            if(foodPics[i].cursor) {
                cursorPic = foodPics[i];
            }
            foodPics[i].draw(this.context);
        }
        if(cursorPic)
            cursorPic.draw(this.context);
        
        
        
        
        for(var i=0; i<arrows.length; i++) {
            arrows[i].draw(this.context);
        }
        
		/*** ON-SCREEN TESTING STATS ***/
		this.context.fillStyle = "white";
        this.context.fillText("X1: " + this.loadedToX1 + "X2: " + this.loadedToX2, 10, 10);
	};
	
	this.init();
	
}
