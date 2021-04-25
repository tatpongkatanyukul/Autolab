#include <iostream>
#include "stonecode.h"

using namespace std;

int main(){
	char scode[3];
	int decoded;

	cout << "Stones: ";
	cin >> scode[0] >> scode[1] >> scode[2];
	decoded = stone(scode);
	
	cout << "Lapses= " << decoded << endl;
	
	return 0;
}

