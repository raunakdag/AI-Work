#include <iostream>
#include <fstream>
#include<string>
#include<time.h>
#include <math.h>
using namespace std;

string image[800][800];

class pixel{
    double x, y;
public:
    pixel(double,double);
    double getX(){return x;};
    double getY(){return y;};
};
pixel::pixel(double xi,double yi){
    x=xi;
    y=yi;
}
void illuminate(double x, double y,string arr[][800]){
    if(x>=0&&x<=800&&y>=0&&y<=800){
        arr[(int)x][(int)y]="1 1 1 ";
    }
}
void line(pixel v1, pixel v2){
    double dx=v2.getX()-v1.getX();
    double dy=v2.getY()-v1.getY();
    double j=v1.getY();
    double e=dy-dx;
    double xinc=1;
    double yinc=1;
    if(abs (dx) >abs (dy)){
        if(dx<0){
            xinc=-1;
        }
        if(dy<0){
            yinc=-1;
        }
        for(int i=v1.getX();i<v2.getX()-1;i=i+xinc){
            illuminate(i,j,image);
            if(e>=0){
                j=j+yinc;
                e=e-(xinc*dx);
            }
            e=e+(yinc*dy);
        }
    }
    else{
        j=v1.getX();
        e=dx-dy;
        if(dy<0){
            yinc=-1;
        }
        if(dx<0){
            xinc=-1;
        }
        for(int i=v1.getY();i<v2.getY()-1;i=i+yinc){
            illuminate(j,i,image);
            if(e>=0){
                j=j+xinc;
                e=e-(yinc*dy);
            }
            e=e+(xinc*dx);
        }
    }

}
void circle(double cx, double cy, double r){
    double xmax=(r*0.70710678);
    double y=r;
    double y2=y*y;
    double ty=(2*y)-1;
    double y2_new=y2;
    for(int x=0;x<=xmax;x++){
        if((y2-y2_new)>=ty){
            y2=y2-ty;
            y=y-1;
            ty=ty-2;
        }
        illuminate(x+cx,y+cy,image);
        illuminate(x+cx,(-1*y)+cy,image);
        illuminate((-1*x)+cx,y+cy,image);
        illuminate((-1*x)+cx,(-1*y)+cy,image);
        illuminate(y+cx,x+cy,image);
        illuminate(y+cx,(-1*x)+cy,image);
        illuminate((-1*y)+cx,x+cy,image);
        illuminate((-1*y)+cx,(-1*x)+cy,image);
        y2_new=y2_new-((2*x)-3);
    }

}
void circumcenter(pixel v1,pixel v2,pixel v3){
    double m1=-1/double(((v2.getY()-v1.getY())/(v2.getX()-v1.getX())));
    double m2=-1/double(((v3.getY()-v2.getY())/(v3.getX()-v2.getX())));
    double px1=(v1.getX()+v2.getX())/2;
    double py1=(v1.getY()+v2.getY())/2;
    double px2=(v2.getX()+v3.getX())/2;
    double py2=(v2.getY()+v3.getY())/2;
    double b1=py1-(m1*px1);
    double b2=py2-(m2*px2);

    double ccx=(b2-b1)/(m1-m2);
    double ccy=(m2*ccx)+b2;

    double d1=sqrt(pow(v2.getX()-v3.getX(),2)+pow(v2.getY()-v3.getY(),2));
    double d2=sqrt(pow(v1.getX()-v3.getX(),2)+pow(v1.getY()-v3.getY(),2));
    double d3=sqrt(pow(v2.getX()-v1.getX(),2)+pow(v2.getY()-v1.getY(),2));

    double s=(d1+d2+d3)/2;
    double r=sqrt(((s-d1)*(s-d2)*(s-d3))/s);
    double R=(d1*d2*d3)/(4*r*s);
    //illuminate(ccx,ccy,image);
    circle(ccx,ccy,R);
}
int main(void) {
    srand(time(0));
    double x1unit=(double)rand()/(double)RAND_MAX;
    double y1unit=(double)rand()/(double)RAND_MAX;
    double x2unit=(double)rand()/(double)RAND_MAX;
    double y2unit=(double)rand()/(double)RAND_MAX;
    double x3unit=(double)rand()/(double)RAND_MAX;
    double y3unit=(double)rand()/(double)RAND_MAX;
    ofstream myfile;
    myfile.open ("triangle.ppm");
    myfile << "P3 800 800 1";
    double x1=(800*x1unit);
    double y1=(800*y1unit);
    double x2=(800*x2unit);
    double y2=(800*y2unit);
    double x3=(800*x3unit);
    double y3=(800*y3unit);
    cout << "x1:"<<x1<<" y1:"<<y1<<" x2:"<<x2<<" y2:"<<y2<<" x3:"<<x3<<" y3:"<<y3;
    pixel v1(x1,y1);
    pixel v2(x2,y2);
    pixel v3(x3,y3);
    for(int i=0;i<800;i=i+1){
        for(int j=0;j<800;j=j+1){
            image[i][j]="0 0 0 ";
        }
    }
    illuminate(v1.getX(),v1.getY(),image);
    illuminate(v2.getX(),v2.getY(),image);
    illuminate(v3.getX(),v3.getY(),image);
    line(v1,v2);
    line(v2,v1);
    line(v2,v3);
    line(v3,v2);
    line(v1,v3);
    line(v3,v1);
    circumcenter(v1,v2,v3);
    double d1=sqrt(pow(v2.getX()-v3.getX(),2)+pow(v2.getY()-v3.getY(),2));
    double d2=sqrt(pow(v1.getX()-v3.getX(),2)+pow(v1.getY()-v3.getY(),2));
    double d3=sqrt(pow(v2.getX()-v1.getX(),2)+pow(v2.getY()-v1.getY(),2));

    double s=(d1+d2+d3)/2;
    double r=sqrt(((s-d1)*(s-d2)*(s-d3))/s);
    double R=(d1*d2*d3)/(4*r*s);

    double icx=((d1*v1.getX())+(d2*v2.getX())+(d3*v3.getX()))/(d1+d2+d3);
    double icy=((d1*v1.getY())+(d2*v2.getY())+(d3*v3.getY()))/(d1+d2+d3);

    //illuminate(icx,icy,image);
    circle(icx,icy,r);
    double px1=(v1.getX()+v2.getX())/2;
    double py1=(v1.getY()+v2.getY())/2;
    double px2=(v2.getX()+v3.getX())/2;
    double py2=(v2.getY()+v3.getY())/2;
    double px3=(v3.getX()+v1.getX())/2;
    double py3=(v3.getY()+v1.getY())/2;
    pixel n1(px1,py1);
    pixel n2(px2,py2);
    pixel n3(px3,py3);
    circumcenter(n1,n2,n3);
    for(int i=0;i<800;i=i+1){
        myfile<<"\n";
        for(int j=0;j<800;j=j+1){
            myfile << image[j][i];
        }
    }
    myfile.close();
    return 0;
}
