#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <malloc.h>
#include "my.h"
#include <opencv2/opencv.hpp>
#define Maxvalue (x>y)?x:y
#define Minvalue (x<y)?x:y
#define endif
#define _CRT_SECURE_NO_WARNINGS
#pragma warnings(disable: 4996)

using namespace cv;


typedef struct {
	int r, g, b;
}int_rgb;


int** IntAlloc2(int height, int width)
{
	int** tmp;
	tmp = (int**)calloc(height, sizeof(int*));
	for (int i = 0; i < height; i++)
		tmp[i] = (int*)calloc(width, sizeof(int));
	return(tmp);
}

void IntFree2(int** image, int height, int width)
{
	for (int i = 0; i < height; i++)
		free(image[i]);

	free(image);
}


float** FloatAlloc2(int height, int width)
{
	float** tmp;
	tmp = (float**)calloc(height, sizeof(float*));
	for (int i = 0; i < height; i++)
		tmp[i] = (float*)calloc(width, sizeof(float));
	return(tmp);
}

void FloatFree2(float** image, int height, int width)
{
	for (int i = 0; i < height; i++)
		free(image[i]);

	free(image);
}

int_rgb** IntColorAlloc2(int height, int width)
{
	int_rgb** tmp;
	tmp = (int_rgb**)calloc(height, sizeof(int_rgb*));
	for (int i = 0; i < height; i++)
		tmp[i] = (int_rgb*)calloc(width, sizeof(int_rgb));
	return(tmp);
}

void IntColorFree2(int_rgb** image, int height, int width)
{
	for (int i = 0; i < height; i++)
		free(image[i]);

	free(image);
}

int** ReadImage(char* name, int* height, int* width)
{
	Mat img = imread(name, IMREAD_GRAYSCALE);  //GRAYSCALE 은 흑백으로 출력하게 하는 것
	int** image = (int**)IntAlloc2(img.rows, img.cols);

	*width = img.cols;
	*height = img.rows;

	for (int i = 0; i < img.rows; i++)
		for (int j = 0; j < img.cols; j++)
			image[i][j] = img.at<unsigned char>(i, j);

	return(image);
}

void WriteImage(char* name, int** image, int height, int width)
{
	Mat img(height, width, CV_8UC1);
	for (int i = 0; i < height; i++)
		for (int j = 0; j < width; j++)
			img.at<unsigned char>(i, j) = (unsigned char)image[i][j];

	imwrite(name, img);
}


void ImageShow(char* winname, int** image, int height, int width)
{
	Mat img(height, width, CV_8UC1);
	for (int i = 0; i < height; i++)
		for (int j = 0; j < width; j++)
			img.at<unsigned char>(i, j) = (unsigned char)image[i][j];
	imshow(winname, img);
	waitKey(0);
}



int_rgb** ReadColorImage(char* name, int* height, int* width)
{
	Mat img = imread(name, IMREAD_COLOR);
	int_rgb** image = (int_rgb**)IntColorAlloc2(img.rows, img.cols);

	*width = img.cols;
	*height = img.rows;

	for (int i = 0; i < img.rows; i++)
		for (int j = 0; j < img.cols; j++) {
			image[i][j].b = img.at<Vec3b>(i, j)[0];
			image[i][j].g = img.at<Vec3b>(i, j)[1];
			image[i][j].r = img.at<Vec3b>(i, j)[2];
		}

	return(image);
}

void WriteColorImage(char* name, int_rgb** image, int height, int width)
{
	Mat img(height, width, CV_8UC3);
	for (int i = 0; i < height; i++)
		for (int j = 0; j < width; j++) {
			img.at<Vec3b>(i, j)[0] = (unsigned char)image[i][j].b;
			img.at<Vec3b>(i, j)[1] = (unsigned char)image[i][j].g;
			img.at<Vec3b>(i, j)[2] = (unsigned char)image[i][j].r;
		}

	imwrite(name, img);
}

void ColorImageShow(char* winname, int_rgb** image, int height, int width)
{
	Mat img(height, width, CV_8UC3);
	for (int i = 0; i < height; i++)
		for (int j = 0; j < width; j++) {
			img.at<Vec3b>(i, j)[0] = (unsigned char)image[i][j].b;
			img.at<Vec3b>(i, j)[1] = (unsigned char)image[i][j].g;
			img.at<Vec3b>(i, j)[2] = (unsigned char)image[i][j].r;
		}
	imshow(winname, img);
	waitKey();

}

template <typename _TP>
void ConnectedComponentLabeling(_TP** seg, int height, int width, int** label, int* no_label)
{

	//Mat bw = threshval < 128 ? (img < threshval) : (img > threshval);
	Mat bw(height, width, CV_8U);

	for (int i = 0; i < height; i++) {
		for (int j = 0; j < width; j++)
			bw.at<unsigned char>(i, j) = (unsigned char)seg[i][j];
	}
	Mat labelImage(bw.size(), CV_32S);
	*no_label = connectedComponents(bw, labelImage, 8); // 0        Ե        

	(*no_label)--;

	for (int i = 0; i < height; i++) {
		for (int j = 0; j < width; j++)
			label[i][j] = labelImage.at<int>(i, j);
	}
}

#define imax(x, y) ((x)>(y) ? x : y)
#define imin(x, y) ((x)<(y) ? x : y)

int BilinearInterpolation(int** image, int width, int height, double x, double y)
{
	int x_int = (int)x;
	int y_int = (int)y;

	int A = image[imin(imax(y_int, 0), height - 1)][(imax(x_int, 0), width - 1)];
	int B = image[imin(imax(y_int, 0), height - 1)][imin(imax(x_int + 1, 0), width - 1)];
	int C = image[imin(imax(y_int + 1, 0), height - 1)][imin(imax(x_int, 0), width - 1)];
	int D = image[imin(imax(y_int + 1, 0), height - 1)][imin(imax(x_int + 1, 0), width - 1)];

	double dx = x - x_int;
	double dy = y - y_int;

	double value
		= (1.0 - dx) * (1.0 - dy) * A + dx * (1.0 - dy) * B
		+ (1.0 - dx) * dy * C + dx * dy * D;

	return((int)(value + 0.5));
}


void DrawHistogram(char* comments, int* Hist)
{
	int histSize = 256; /// Establish the number of bins
	// Draw the histograms for B, G and R
	int hist_w = 512; int hist_h = 512;
	int bin_w = cvRound((double)hist_w / histSize);

	Mat histImage(hist_h, hist_w, CV_8UC3, Scalar(255, 255, 255));
	Mat r_hist(histSize, 1, CV_32FC1);
	for (int i = 0; i < histSize; i++)
		r_hist.at<float>(i, 0) = Hist[i];
	/// Normalize the result to [ 0, histImage.rows ]
	normalize(r_hist, r_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat());

	/// Draw for each channel
	for (int i = 1; i < histSize; i++)
	{
		line(histImage, Point(bin_w * (i - 1), hist_h - cvRound(r_hist.at<float>(i - 1))),
			Point(bin_w * (i), hist_h - cvRound(r_hist.at<float>(i))),
			Scalar(255, 0, 0), 2, 8, 0);
	}

	/// Display
	namedWindow(comments, WINDOW_AUTOSIZE);
	imshow(comments, histImage);

	waitKey(0);

}

//11.16 수능날

// //흑백
// float MAD(int** A, int** B, int dy, int dx)
// {
// 	float mad = 0.0;

// 	for (int y = 0; y < dy; y++) {
// 		for (int x = 0; x < dx; x++) {
// 			mad += abs(A[y][x] - B[y][x]);
// 		}
// 	}
// 	return mad / (dy * dx);
// }
// //컬러
// float MAD_Color(int_rgb** A, int_rgb** B, int dy, int dx)
// {
// 	float mad = 0.0;

// 	for (int y = 0; y < dy; y++) {
// 		for (int x = 0; x < dx; x++) {
// 			mad += abs(A[y][x].r - B[y][x].r);
// 			mad += abs(A[y][x].g - B[y][x].g);
// 			mad += abs(A[y][x].b - B[y][x].b);
// 			// 얘는 따로따로해줘야함
// 		}
// 	}
// 	return mad / (dy * dx);
// }
// //
// //#define SQ(x) (x * x)
// //float MSE(int** A, int** B, int dy, int dx)
// //{
// //	float mse = 0.0;
// //
// //	for (int y = 0; y < dy; y++) {
// //		for (int x = 0; x < dx; x++) {
// //			//mse += abs(A[y][x] - B[y][x]) * abs(A[y][x] - B[y][x]);
// //			mse += SQ(A[y][x] - B[y][x]);
// //		}
// //	}
// //	return mse / (dy * dx);
// //}
// //
// //흑백
// void ReadBlock(int** img, int y0, int x0, int dy, int dx, int** block)
// {
// 	for (int y = 0; y < dy; y++) {
// 		for (int x = 0; x < dx; x++) {
// 			block[y][x] = img[y0 + y][x0 + x];
// 		}
// 	}
// }
// //컬러
// void ReadColorBlock(int_rgb** img, int y0, int x0, int dy, int dx, int_rgb** block)
// {
// 	for (int y = 0; y < dy; y++) {
// 		for (int x = 0; x < dx; x++) {
// 			//block[y][x].r = img[y0 + y][x0 + x].r;
// 			block[y][x].r = img[y0 + y][x0 + x].r;
// 			block[y][x].g = img[y0 + y][x0 + x].g;
// 			block[y][x].b = img[y0 + y][x0 + x].b;
// 		    // C++ 플랫폼이라서 하나만 해줘도 된대... 십사기
// 		}
// 	}
// }

// //흑백
// void WriteBlock(int** img, int y0, int x0, int dy, int dx, int** block)
// {
// 	for (int y = 0; y < dy; y++) {
// 		for (int x = 0; x < dx; x++) {
// 			img[y0 + y][x0 + x] = block[y][x];
// 		}
// 	}
// }

// //컬러
// void WriteColorBlock(int_rgb** img, int y0, int x0, int dy, int dx, int_rgb** block)
// {
// 	for (int y = 0; y < dy; y++) {
// 		for (int x = 0; x < dx; x++) {
// 			img[y0 + y][x0 + x].r = block[y][x].r;
// 			img[y0 + y][x0 + x].g = block[y][x].g;
// 			img[y0 + y][x0 + x].b = block[y][x].b;
// 			//이것도 그냥 이렇게 두면 된다..
// 		}
// 	}
// }
// //
// //int ex11_16()
// //{
// //
// //	int height, width;
// //	int** img = ReadImage((char*)"lena.png", &height, &width);
// //	int** img_out = (int**)IntAlloc2(height, width);
// //	int dy = 32, dx = 32;
// //	int** block = (int**)IntAlloc2(dy, dx);
// //
// //	ReadBlock(img, 100, 200, dy, dx, block);
// //	WriteImage((char*)"template.jpg", block, dy, dx);
// //
// //	//ImageShow((char*)"output", img_out, height, width);
// //	
// //	return 0;
// //}
// //
// //void CopyImage(int** img, int height, int width, int** img_out)
// //{
// //	for (int y = 0; y < height; y++) for (int x = 0; x < width; x++)  img_out[y][x] = img[y][x];
// //}
// //
// //void DrawBBox(int** img, int height, int width, int y0, int x0, int dy, int dx, int** img_out)
// //{
// //	CopyImage(img, height, width, img_out);
// //
// //	for (int x = 0; x < dx; x++) {
// //		img_out[y0][x0 + x] = 255;
// //		img_out[y0 + dy][x0 + x] = 255;
// //	}
// //
// //	for (int y = 0; y < dy; y++) {
// //		img_out[y0 + y][x0] = 255;
// //		img_out[y0 + y][x0 + dx] = 255;
// //	}
// //}
// //
// //struct Point2D {
// //	int x;
// //	int y;
// //};
// //
// //
// //Point2D TemplateMatching(int** img, int height, int width, int** tmp, int dy, int dx)
// //{
// //	float mad_min = INT_MAX;
// //	int y_min = 0, x_min = 0;
// //	int** block = (int**)IntAlloc2(dy, dx);
// //
// //	//10분이나 시간을 주는 문제 . . . . 
// //	for (int y0 = 0; y0 < height - dy / 2; y0++) {
// //		for (int x0 = 0; x0 < width - dx / 2; x0++) {
// //
// //			ReadBlock(img, y0, x0, dy, dx, block);
// //			float mad = MAD(block, tmp, dy, dx);
// //			if (mad < mad_min) {
// //				mad_min = mad;
// //				y_min = y0;
// //				x_min = x0;
// //			}
// //		}
// //	}
// //	IntFree2(block, dy, dx);
// //
// //	Point2D P;
// //	P.x = x_min;
// //	P.y = y_min;
// //
// //	return P;
// //}
// //
// //int main()
// //{
// //	int height, width;
// //	int** img = ReadImage((char*)"lena.png", &height, &width);
// //	int dy, dx;
// //	int** tmp = ReadImage((char*)"template.jpg", &dy, &dx);
// //	int** img_out = (int**)IntAlloc2(height, width);
// //
// //	Point2D P = TemplateMatching(img, height, width, tmp, dy, dx);
// //
// //	DrawBBox(img, height, width, P.y, P.x, dy, dx, img_out);
// //
// //	ImageShow((char*)"input", img, height, width);
// //	ImageShow((char*)"output", img_out, height, width);
// //
// //	return 0;
// //}

// //11월 20일
// //11월 23일은 메인함수 + FindSingleBlock로부터 시작
// #define M 510

// //흑백
// int FindOptIndex(int** block, int*** db, int dy, int dx )
// {
// 	float mad_min = INT_MAX;    // 최소를 구할 때는 최대로 설정한다.
// 	int save_i = 0;
// 	for (int i = 0; i < M; i++) {
// 		float mad = MAD(block, db[i], dy, dx);
// 		if (mad < mad_min) {
// 			mad_min = mad;    // 최소값을 바꿔주고 해당 인덱스까지 저장해야함
// 			save_i = i;
// 		}
// 	}
// 	return save_i;
// }
// //컬러
// int FindOptIndexColor(int_rgb** block, int_rgb*** db, int dy, int dx)
// {
// 	float mad_min = INT_MAX;    // 최소를 구할 때는 최대로 설정한다.
// 	int save_i = 0;
// 	for (int i = 0; i < M; i++) {
// 		float mad = MAD_Color(block, db[i], dy, dx);
// 		if (mad < mad_min) {
// 			mad_min = mad;    // 최소값을 바꿔주고 해당 인덱스까지 저장해야함
// 			save_i = i;
// 		}
// 	}
// 	return save_i;
// }

// //흑백
// void MosaicSingleBlock(int y0, int x0, int dy, int dx, int db_size, int*** db, int** img, int** img_out)
// {
// 	int** block = (int**)IntAlloc2(dy, dx);  // int** --> int_rgb**

// 	ReadBlock(img, y0, x0, dy, dx, block); // -> ReadColorBlock()

// 	int OptIndex = FindOptIndex(block, db, dy, dx);  // ColorMAD()

// 	WriteBlock(img_out, y0, x0, dy, dx, db[OptIndex]);  // WriteColorBlock()

// 	IntFree2(block, dy, dx); // IntColorFree2()
// }
// //컬러
// void MosaicColorSingleBlock(int y0, int x0, int dy, int dx, int db_size, int_rgb*** db, int_rgb** img, int_rgb** img_out)
// {
// 	int_rgb** Color_block = (int_rgb**)IntColorAlloc2(dy, dx);

// 	ReadColorBlock(img, y0, x0, dy, dx, Color_block);

// 	int OptIndex = FindOptIndexColor(Color_block, db, dy, dx);  // ColorMAD()

// 	WriteColorBlock(img_out, y0, x0, dy, dx, db[OptIndex]);  // WriteColorBlock()

// 	IntColorFree2(Color_block, dy, dx); // IntColorFree2()
// }

// //흑백
// void MosaicImage(int dy, int dx, int db_size, int*** db, int** img, int height, int width, int** img_out)
// {
// 	int y0 = dy, x0 = 0;
// 	for (int y = 0; y < height; y += dy) {
// 		for (int x = 0; x < width; x += dx) {
// 			MosaicSingleBlock(y, x, dy, dx, db_size, db, img, img_out);     //M = db_size
// 		}
// 	}
// }

// //컬러
// void MosaicColorImage(int dy, int dx, int db_size, int_rgb*** db, int_rgb** img, int height, int width, int_rgb** img_out)
// {
// 	int y0 = dy, x0 = 0;
// 	for (int y = 0; y < height; y += dy) {
// 		for (int x = 0; x < width; x += dx) {
// 			MosaicColorSingleBlock(y, x, dy, dx, db_size, db, img, img_out);     //M = db_size
// 		}
// 	}
// }

// //흑백
// void MakeSmallDB(int*** db, int dy, int dx, int db_size, int*** img_out)
// {
// 	for (int y = 0; y < dy; y += 2) {
// 		for (int x = 0; x < dx; x += 2) {
// 			img_out[y / 2][x / 2] = db[y][x];
// 		}
// 	}
// }
// //컬러
// void MakeColorSmallDB(int_rgb*** db, int dy, int dx, int db_size, int_rgb*** img_out)
// {
// 	for (int y = 0; y < dy; y += 2) {
// 		for (int x = 0; x < dx; x += 2) {
// 			img_out[y / 2][x / 2] = db[y][x];
// 		}
// 	}
// }
int
// //int main()
// //{
// //	int height, width;
// //	int** img = ReadImage((char*)"lena.png", &height, &width);
// //	int** img_out = (int**)IntAlloc2(height, width);
// //	int** db[M];
// //	int dy, dx;
// //	char db_name[100];
// //
// //	for (int i = 0; i < M; i++) {
// //		sprintf_s(db_name, "./db영상(얼굴)/dbs%04d.jpg", i);    //디렉터리 위에 없는 폴더에서 가지고올 때 ./폴더이름/사진이름.jpg 로 하거나 \\폴더이름\\/사진이름으로 하거나
// //		db[i] = ReadImage(db_name, &dy, &dx);
// //		
// //	}
// //
// //	int** s_db[M];
// //	for (int i = 0; i < M; i++) {
// //		s_db[i] = (int**)IntAlloc2(dy / 2, dx / 2);
// //	}
// //	MakeSmallDB(db, dy, dx, M, s_db);
// //
// //	//MosaicImage(dy, dx, M, db, img, height, width, img_out);
// //	MosaicImage(dy / 2, dx / 2, M, s_db, img, height, width, img_out);
// //
// //	ImageShow((char*)"output", img_out, height, width);
// //	return 0;
// //}

// //int main()
// //{
// //	int_rgb A, B[3];
// //	int_rgb C[10][5];
// //
// //	A.b = 100;
// //	A.g = 200;
// //	A.r = 150;
// //
// //	B[0].b = 100;
// //	B[0].g = 200;
// //	B[0].r = 110;
// //
// //	C[1][3].r = 100;
// //
// //	return 0;
// //}

// int main()
// {
// 	int height, width;
// 	int_rgb** img = ReadColorImage((char*)"food3.png", &height, &width);
// 	int_rgb** img_out = ((int_rgb**)IntColorAlloc2(height, width));
// 	int_rgb** db[M];
// 	int dy, dx;       // int_rgb dy, dx 아님 주의 //
// 	char db_name[100];

// 	for (int i = 0; i < M; i++) {
// 		sprintf_s(db_name, "./db영상(얼굴)/dbs%04d.jpg", i);    //디렉터리 위에 없는 폴더에서 가지고올 때 ./폴더이름/사진이름.jpg 로 하거나 \\폴더이름\\/사진이름으로 하거나
// 		db[i] = ReadColorImage(db_name, &dy, &dx);
// 	}

// 	int_rgb** s_db[M];
// 	for (int i = 0; i < M; i++) {
// 	    s_db[i] = (int_rgb**)IntColorAlloc2(dy / 2, dx / 2);
// 	}
// 	MakeColorSmallDB(db, dy, dx, M, s_db);

// 	MosaicColorImage(dy / 2, dx / 2, M, s_db, img, height, width, img_out);

// 	ColorImageShow((char*)"input", img, height, width);
// 	ColorImageShow((char*)"output", img_out, height, width);
	
// 	return 0;
// }
#define M 510

//이미지 두 개의 픽셀간 유사도 측정 절댓값의 합사용
float MAD(int** img1, int** img2, int height, int width)
{
    float mad = 0.0;
    for (int y = 0; y < height; y++){
        for (int x = 0; x < width; x++){
            mad += abs(img1[y][x] - img2[y][x]);
        }
    }

    return (mad / (heght * width));  //총 개수로 나눔
}

//이미지 두 개의 픽셀간 유사도 측정 제곱의 합 사용
float MSE(int** img1, int** img2, int height, int width)
{
    float mse = 0.0;
    for (int y = 0; y < height; y++){
        for (int x = 0; x < width; x++){
            mse += (img1[y][x] - img2[y][x]) * (img1[y][x] - img2[y][x]);
        }
    }

    return (mse / (heght * width));  //총 개수로 나눔
}

float MAD2(int yp, int xp, int dy, int dx, int** template, int** img, int height, int width)
{
    float mad = 0.0;
    for (int y = 0; y < dy; y++){
        for (int x = 0; x < dx; x++){
            mad += abs(template[y][x] - img[yp + y][xp + x]);
        }
    }

    return (mad / (dy * dx));
}

int main()
{
    int height, width;
    int** img = ReadImgage((char*)"lena.png", &height, &width);
    int** db[M];
    int** img_out = (int**)IntAlloc2(height, width);

    int dy, dx;
    char db_name[100];

    for(int i = 0; i < M; i++){
        sprintf_s(db_name, "./db영상(얼굴)/dbs%04d.jpg", i);    //디렉터리 위에 없는 폴더에서 가지고올 때 ./폴더이름/사진이름.jpg 로 하거나 \\폴더이름\\/사진이름으로 하거나
        db[i] = ReadImage(db_name, &dy, &dx);
    }



}