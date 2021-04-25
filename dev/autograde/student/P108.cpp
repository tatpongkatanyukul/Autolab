#include <iostream>
#include <fstream>
#include <iomanip>

using namespace std;

int main(){
	string ipfname, opfname;
	float vat;
	float aftertax, beforetax, tax;
	
	cout << "Input file: ";
	cin >> ipfname;
	cout << "Output file: ";
	cin >> opfname;
	cout << "Vat: ";
	cin >> vat;
	
	ifstream fin(ipfname);
	ofstream fout(opfname);
	
	fout << fixed << setprecision(2);
	
	while(fin >> aftertax){
		beforetax = aftertax * 100/(100 + vat);
		tax = beforetax * vat/100;
		fout << beforetax << " + " << tax << " = " << aftertax << endl;
	}
	
	cout << opfname << " is ready." << endl;

return 0;
}