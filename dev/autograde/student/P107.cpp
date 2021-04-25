#include "stonecode.h"

#include <iostream>
using namespace std;

int c2i(char c){
	
	return c - 48;
}

int stone(char code[3]){
	int d;
	
	//cout << "stone: code=" << code[0] << code[1] << code[2] << endl;
	//cout << int(code[0]) - 48 << endl;
	//cout << int(code[1]) - 48 << endl;
	//cout << int(code[2]) - 48 << endl;
	//cout << c2i(code[0]) << endl;
	
	d = c2i(code[0])*9 + c2i(code[1])*3 + c2i(code[2]);
	
	return d;
}
