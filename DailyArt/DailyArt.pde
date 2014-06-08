/*
  This app takes an image that is already in our download folder
  and then manipulate the image randomly.
  
  */

PImage img;
int x,y;
int curvePointX = 0;
int curvePointY = 0;
int pointCount = 1;
int loopNum = 0;
int numOpp = 100;
float lineWeight = 0;
float diffusion = 50;
boolean save = false;
boolean pause = false;
boolean drawLines = false;
boolean drawSmLines = false;
boolean drawCurves = false;
boolean smCurves = false;
boolean smLines = false;
boolean showTint = false;
int loopNumLine = 0;
int numOppLine = 100;
int timeToRun = 10000;

// Agents - not sure we'll keep
// ------ agents ------
Agent[] agents = new Agent[int(random(100,1000))];
int agentsCount = 4000;
float noiseScale = 100, noiseStrength = 10, noiseZRange = 0.4;
float overlayAlpha = 10, agentsAlpha = 90, strokeWidth = 0.3;
int drawMode = 1;
// end Agents

void setup(){
  //textsize(32);
  img = loadImage("../newImage/newImage.jpg");
  size(img.width, img.height);
  x = width/2;
  y = height/2;
  dailyRandom();  
  image(img,0,0);
  
  // Create the Agents
  for(int i=0; i<agents.length; i++) agents[i] = new Agent();
}

void draw(){
  
  colorMode(HSB, 360,100,100);    
  smooth();
  noFill();
  
// Draw the original window
//  imageFrame.draw();

// How long to run for
for(int i=0; i<timeToRun; i++) {
  int pixelIndex = ( x+ (y*img.width ));
  color c = img.pixels[pixelIndex];
  color(c,random(1,255));
  // The last random function adds more thickness to the line
  lineWeight = hue(c)/(int)random(30,50) * random(1,day()); // Day of the week for the random size was 5  
  strokeWeight(lineWeight/month()); // month // was 2
  
  // Every 100 times - get the opposite color
  if( loopNum == numOpp) {
    loopNum = 0;
    float R = red(c);
    float G = green(c);
    float B = blue(c);
    float minRGB = min(R,min(G,B));
    float maxRGB = max(R,max(G,B));
    float minPlusMax = minRGB + maxRGB;
    color complement = color(minPlusMax-R, minPlusMax-G, minPlusMax-B);
    stroke(complement);
  } else {
    stroke(c);
    loopNum ++;
  }
  
// how to draw
// Default all to true to start
//  drawLines = true;
//  drawSmLines = true;
//  drawCurves = true;
  if(!pause) {
    if( drawLines ) {
      drawLines();
    }
    if(drawSmLines) {
      drawSmallLines();
    }
    if(drawCurves) {
      drawCurves();
    }
  }


if((int)random(1,5) < 3){
  drawLines();
}
if ((int)random(1,5) ==3) {
  drawSmallLines();
}
if ((int)random(1,5) > 3) {
  drawCurves();
}

  // change the size
  pointCount = (int)random(1,5);
} // timeToRun

// This loop is all new - I really like this - but maybe I'll use it for the hourly pic instead
// Now loop another x times and draw straight lines on top
// takes the last used color - ok?
//for(int j = 0; j < int(random(1000,200000)); j++){
//  drawStraightLines();
//  pointCount = (int)random(1,5);
//}

// Now that the initial image is done - run the Agents!
// Which type
int type = int(random(1,2));
int time_to_run = int(random(10,200));
for(int j = 0; j < time_to_run; j++){ 
  if(type ==1) {
  for(int i=0; i<agents.length; i++) 
    agents[i].update1();
    int pixelIndex = ( x+ (y*img.width ));
  color c = img.pixels[pixelIndex];
  color(c,random(1,255)); 
  stroke(color(c,random(1,255)));
    pointCount = (int)random(1,5);
    x = (int)random(0, width);
    y  = (int)random(0, height);
  } 
  else {
    for(int i=0; i<agentsCount; i++) 
        agents[i].update2();
      int pixelIndex = ( x+ (y*img.width ));
  color c = img.pixels[pixelIndex];
  color(c,random(1,255));
 stroke(color(c,random(1,255))); 
    pointCount = (int)random(1,5);
    x = (int)random(0, width);
    y  = (int)random(0, height);
  } 

}

  save("/newImage/newImageChanged.jpg");
  exit();
}



void drawSmallLines(){
  strokeWeight(random(.1,3));
  if (loopNumLine >= numOppLine) {
    if(smLines){
      line(x,y, x+ random(-width, width)/8, y + random(-height, height)/8);
    } else {
      line(x,y, x+ random(-width, width)/2, y + random(-height, height)/2);
    }
    loopNumLine = 0;
  } else {
    line(x, y, x+ random(3,30), y+ random(3,30));
    loopNumLine = loopNumLine + (int)random(-1,5);
    x = (int)random(0, width);
    y  = (int)random(0, height);
  }
}

void drawCurves() {
    // every numOpp times - do a stright line
  if( loopNumLine >= numOppLine ) {
    if(smLines){
      line(x,y, x+ random(-width, width)/8, y + random(-height, height)/8);
    } else {
      line( x, y, x + random(-width,width)/2, y + random(-height,height)/2);
    }
    loopNumLine = 0;
    //printText("Line!!!!!!!!!!!!!!!!!!!!!",10,20);
  } else {
    beginShape();
    curveVertex(x,y);
    curveVertex(x,y);
    for( int i = 0; i<pointCount; i++) {
      if(smCurves) {
        curvePointX = (int)constrain(x+random(-10, 10), 0, width-1);
        curvePointY = (int)constrain(y+random(-10,10),0, height-1);        
      } else {
        curvePointX = (int)constrain(x+random(-50, 50), 0, width-1);
        curvePointY = (int)constrain(y+random(-50,50),0, height-1);
      }
      curveVertex(curvePointX, curvePointY);
    }   
    curveVertex(curvePointX, curvePointY);
    endShape();
    x = curvePointX;
    y = curvePointY;
    loopNumLine = loopNumLine + (int)random(-1,5);
  }
}

void drawLines() {
  if (loopNumLine >= numOppLine) {
    if(smLines){
      line(x,y, x+ random(-width, width)/8, y + random(-height, height)/8);
    } else {
      line(x,y, x+ random(-width, width)/2, y + random(-height, height)/2);
    }
    loopNumLine = 0;
  } else {
    line(x, y, x+ random(1,10), y+ random(1,10));
    loopNumLine = loopNumLine + (int)random(-1,5);
    x = (int)random(0, width);
    y  = (int)random(0, height);
  }
   
}

void drawStraightLines() {
    line(x, y, x+ random(3,30), y+ random(3,30));
    loopNumLine = loopNumLine + (int)random(-1,5);
    x = (int)random(0, width);
    y  = (int)random(0, height);
}


void printText(String text, int locationX, int locationY) {
  //text(text, locationX, locationY);
  println(text);
}

// timestamp
String timestamp() {
  //Calendar now = Calendar.getInstance();
  //return String.format("%1$ty%1$tm%1$td_%1$tH%1$tM%1$tS", now);
  return "";
}

void dailyRandom(){
  // Here we will change the values depending on external info
  timeToRun = int(random(10000, 200000)); // This needs to be random
}
