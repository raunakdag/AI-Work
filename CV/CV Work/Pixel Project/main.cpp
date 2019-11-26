#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <math.h>
using namespace std;

const int width = 800, height = 800;
const string white = "255 255 255 ";
const string black = "0 0 0 ";

string points_string_array[width][height];

class Point{
public:
    int x;
    int y;

    void setCoords(int x1, int y1){
        x = x1;
        y = y1;
    }

    int getX(){
        return x;
    }

    int getY(){
        return y;
    }
};

double fRand(){
    return (double)rand() / RAND_MAX;
}

int main(){
    cout << "Hello";
    // CREATE IMAGE STREAM
    ofstream img("main.ppm");
    img << "P3" << " ";
    img << width << " " << height << " ";
    img << "255" << endl;

    // SET ALL POINTS TO WHITE
    for (int h = 0; h < height; h++) {
        for (int w = 0; w < height; w++) {
            points_string_array[h][w] = white;
        }
    }

    Point allPoints[40] = {};
    for(int i = 0; i < 40; i++){
        Point temp;
        temp.setCoords((int)(fRand()*800), (int)(fRand()*800));
        allPoints[i] = temp;
        points_string_array[temp.getX()][temp.getY()] = black;
        points_string_array[temp.getX()+1][temp.getY()] = black;
        points_string_array[temp.getX()][temp.getY()+1] = black;
        points_string_array[temp.getX()+1][temp.getY()+1] = black;
    }

    for()

    // DRAWS TO PPM
    for (int h = 0; h < height; h++) {
        for (int w = 0; w < height; w++) {
            img << points_string_array[w][h];
        }
        img << "\n";
    }



}