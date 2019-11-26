#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <math.h>
using namespace std;

const int width = 800, height = 800;
const string white = "255 255 255 ";
const string black = "0 0 0 ";

string points[width][height];

class Point{
public:
    double coords [2] = {};
    void setCoords(double x, double y){
        coords[0] = x;
        coords[1] = y;
    }

    double getX(){
        return coords[0];
    }

    double getY(){
        return coords[1];
    }
};

double fRand(){
    return (double)rand() / RAND_MAX;
}

void changeToWhite(double x, double y, string arr[][height]){
    if(x >= 0 && x <= width && y >=0 && y <= height){
        arr[(int)x][(int)y] = white;
    }
}

// ASSUMES X1 < X2
void bresenham(Point p1, Point p2){
    // double slope = (double)(p2.coords[1] - p1.coords[1]) / (double)(p2.coords[0] - p1.coords[0]);
    double dx = p2.getX() - p1.getX(); // CHANGE IN X
    double dy = p2.getY() - p1.getY(); // CHANGE IN Y
    double point1_y = p1.getY(); // FIRST COORDS Y
    double e = dy - dx;
    double xinc = 1;
    double yinc = 1;
    if (abs (dx) > abs (dy)){
        if (dx < 0){
            xinc = -1;
        }
        if (dy < 0){
            yinc = -1;
        }
        for (int i = p1.getX(); i < p2.getX() - 1; i = i + xinc){
            changeToWhite(i, point1_y, points);
            if (e >= 0){
                point1_y += yinc;
                e = e - (xinc * dx);
            }
            e = e + (yinc * dy);
        }
    }
    else{
        point1_y = p1.getX();
        e = dx - dy;
        if (dy < 0){
            yinc = -1;
        }
        if (dx < 0){
            xinc = -1;
        }
        for (int i = p1.getY(); i < p2.getY() - 1; i = i + yinc){
            changeToWhite(point1_y, i, points);
            if(e >= 0){
                point1_y += xinc;
                e = e - (yinc * dy);
            }
            e = e + (xinc * dx);
        }
    }
}


int main(void) {
    // CREATE IMAGE STREAM
    ofstream img("main.ppm");
    img << "P3" << " ";
    img << width << " " << height << " ";
    img << "255" << endl;


    // RANDOM
    srand(time(0));




    // GET DECIMAL AND INTEGER COORDINATES OF TRIANGLE
    double decimalCoords[6] = {fRand(), fRand(), fRand(), fRand(), fRand(), fRand()};
    // int intCoords [6] = {};
    for(int x = 0; x < 6; x++){
        decimalCoords[x] = (decimalCoords[x] * width);
        cout << decimalCoords[x];
        cout << " ";
    }


    // SET ALL POINTS TO WHITE
    for (int h = 0; h < height; h++) {
        for (int w = 0; w < height; w++) {
            points[h][w] = white;
        }
    }



    Point p1;
    p1.setCoords(decimalCoords[0], decimalCoords[1]);
    Point p2;
    p1.setCoords(decimalCoords[2], decimalCoords[3]);
    Point p3;
    p1.setCoords(decimalCoords[4], decimalCoords[5]);
    bresenham(p1, p2);
    bresenham(p2, p1);
    bresenham(p2, p3);
    bresenham(p3, p2);
    bresenham(p1, p3);
    bresenham(p3, p1);


    // DRAWS TO PPM
    for (int h = 0; h < height; h++) {
        for (int w = 0; w < height; w++) {
            img << points[w][h];
        }
        img << "\n";
    }

}