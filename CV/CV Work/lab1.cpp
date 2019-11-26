#include <iostream>
#include <fstream>
using namespace std;

const int width = 800, height = 800;

double fRand(){
    double f = (double)rand() / RAND_MAX;
    return 0.0 + f * (1.0 - 0.0);
}

int main(void){
    ofstream img ("main.ppm");
    img << "P3" << " ";
    img << width << " " << height << " ";
    img << "255" << endl;
    int n = 0;

    for(int h = 0; h < height; h++){
        for(int w = 0; w < height; w++){
            int r = h % 255;
            int g = w % 255;
            int b = h * w % 255;

            img << r << " " << g << " " << b << "
        }
        img << endl;
    }

    double coords [6] = { fRand(), fRand(), fRand(), fRand
            for(n = 0; n<6; n++){
                cout << coords[n];
                cout << "\n";
            }
    }