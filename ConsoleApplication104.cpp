#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <cmath>
#include <utility>
#include <set>
#include <string>
#include <queue>
#include <tuple>
using namespace std;

#define vi vector<int>
#define vb vector<bool>
#define pb push_back
#define ll long long
#define vvi vector<vi>
#define pii pair<int, int>
#define mp make_pair
#define vvpii vector<vector<pii>>
#define all(x) x.begin(), x.end()
const int INF = 2e18, MOD = 1e9 + 7;

// obvious: green for one-way intersections
//also "throw" away not used roads.

// we can check what cars we can "throw" away. we sum the weights of its way, and compare to T.
// 

int findStreetIndex(vector<string> streets, string name) {
	int i = 0;
	while (i < streets.size())
	{
		if (!streets[i].compare(name)) {
			break;
		}
		i++;
	}
	return i;
}

int main(){ 

	int D, I, S, V, F;
	cin >> D; //D: duration of the simulation
	cin >> I; //I: the number of intersections
	cin >> S; //S: the number of streets
	cin >> V; //V: the number of cars
	cin >> F; //F: the bonus points for each car that reaches its destination before time

	vector<string> s_names(S); // 2 - rotten child
	vector<pii> streets_co(S); // 2 - (911, 69)
	vi streets_len(S); //2 - L = 1


	for (int i = 0; i < S; i++)
	{
		//B - begining intersection
		//E - end intersection
		//L - length of street
		int B, E, L;
		string str;
		cin >> B;
		cin >> E;
		cin >> str;
		cin >> L;
		s_names[i] = str;
		auto t = mp(B, E);
		streets_co[i] = t;
		streets_len[i] = L;
	}

	vvi cars_paths(V);
	for (int car_index = 0; car_index < V; car_index++)
	{
		int len_path_of_car;
		cin >> len_path_of_car;
		vi path(len_path_of_car);
		for (int j = 0; j < len_path_of_car; j++)
		{
			string street_name;
			cin >> street_name;
			int indexOfStreet = findStreetIndex(s_names, street_name);
			path[j] = indexOfStreet;
		}
		cars_paths[car_index] = path;
	}

	vi path_of_first_car = cars_paths[0];
	// the number of streets the car had been thorugh - 1
	int numOfIntersections = path_of_first_car.size() - 1;

	string output = to_string(numOfIntersections) + '\n';
	for (int index_in_path = 0; index_in_path < numOfIntersections; index_in_path++) {
		int indexOfStreet = path_of_first_car[index_in_path];
		string street_name = s_names[indexOfStreet];
		int intersectionToOpen = streets_co[indexOfStreet].second;
		// how many streets we open in the intersection (1)
		output += to_string(intersectionToOpen) + "\n1\n";
		// 
		output += street_name + " 1\n";
	}
	cout << "======================" << endl;
	cout << output;

	ofstream myfile;
	myfile.open("output_ur_mama.txt");
	myfile << output;
	myfile.close();
}

/*
andddddd
the washington wizards
the best defensive team in the leauge
getting the ball
danny ovadia is getting the ball
what's gonna do danny ovadia
dancing with the ball danny ovadia
THREE POINTSSSSSSSS
YESSSSSSSSS
SHABAT SHALOM
SHAWARMA BEPITZA
BELLAFA
ARBA BE'ESER
ARBA BE'ESER
RAK HAYOM
ATA MAKHISH KORONA AHI
LEMI ATA MATZBIA
SAAR, BENNET?
RAK BIBI!
ATA YAHOL LA'ASOT LI ANAHA?
ANI LO YAHOL HAIOM AHI
YALLA TA'ASE MEHIR MA KARA ANI LAKOH KAVUA
TASIM LI PARGIT IM AMBA BAPITA
YESH BOREKAS GVINA?
MA RAK TERED?
ANI ROTZE PITRIOT!
AHI ATA HOFER
LAMA RAMI VERED BA'AH HAGADOL TASBIRU LI
MA YESH SEGER?
AVAL YESH HISUNIM LAMA SEGER
HAKALKALA CORESET
MI YETAKEN
MI YETAKEN, NISINKER?
NISINKER?
SHABAT SHALOM!
*/
