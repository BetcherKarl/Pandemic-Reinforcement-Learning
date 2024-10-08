#include <string>
#include <vector>

namespace pandemic {
	class City {
	public:
		City(string name, Color color, int population, float position[2]) {
			this->name = name;
			this->color = color;
			this->population = population;
			this->research_station = false;
			this->outbroken = false;
			this->quarantined = false;
			this->position = position;
		}

		// getters and setters
		string getName{ return name; }
		Color getColor{ return color; }
		bool hasResearchStation{ return research_station; }
		vector<City> getNeighbors{ return neighbors; }
		bool isOutbroken{ return outbroken; }
		bool isQuarantined{ return quarantined; }
		float getPosition{ return position; }

		// methods
		void addNeighbor(City other) { neighbors.push_back(other); }

		void addDiseaseCubes(Color color, int num) {
			if (!quarantined) {
				int key = color.key;
				int curr = disease_cubes[key];

				if (num <= 0) {
					throw invalid_argument("Invalid number of cubes to add. Must add at least 1 cube");
				}
				if (num > 24) {
					throw invalid_argument("Too many cubes to add to " + name);
				}

				// too many cubes placed on city causes an outbreak
				if (curr + num > 3) {
					if (!outbroken) {
						disease_cubes[key] = 3;
						outbroken = true;
						outbreak();
					}
				}

				// normal cube add
				disease_cubes[key] += color.takeCubes(num);
			}
		}

		void removeDiseaseCubes(Color color, int num) {
			int key = color.key;
			int curr = disease_cubes[key];

			if (num <= 0) {
				throw invalid_argument("Invalid number of cubes to remove. Must remove at least 1 cube");
			}
			if (num > curr) {
				throw invalid_argument("Not enough cubes to remove from " + name);
			}

			disease_cubes[key] -= color.returnCubes(num);
		}

		void placeResearchStation() { research_station = true; }

	private:
		string name;
		Color color;
		int population;
		bool research_station;
		vector<City> neighbors;
		bool outbroken;
		bool quarantined;
		float position[2];
		vector<int> disease_cubes; // The number of disease cubes for each color, stored by index from Color Object

		void outbreak() {
			for (City neighbor : neighbors) {
				neighbor.addDiseaseCubes(color, 1);
			}
		}
	};
}